import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from typing import List, Dict
from abc import ABC, abstractmethod
from SvdpGrantAgent.schema import GrantRecord, GrantStatus
from SvdpGrantAgent.guardrails import Guardrails

class BaseScraper(ABC):
    @abstractmethod
    def scrape(self) -> List[GrantRecord]:
        pass

class GenericScraper(BaseScraper):
    def __init__(self, url: str, foundation_name: str):
        self.url = url
        self.foundation_name = foundation_name

    def scrape(self) -> List[GrantRecord]:
        """
        Scrapes a webpage for grant-related links.
        """
        try:
            response = requests.get(self.url, timeout=15)
            if response.status_code != 200:
                print(f"Failed to fetch {self.url} (Status: {response.status_code})")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Network error fetching {self.url}: {e}")
            return []
        
        # Guardrail: Sanitize HTML content before parsing
        sanitized_html = Guardrails.sanitize_html(response.text)
        soup = BeautifulSoup(sanitized_html, 'html.parser')
        
        grants = []
        
        # Look for links containing grant-related keywords
        keywords = ['grant', 'funding', 'award', 'program', 'apply', 'opportunity']
        for link in soup.find_all('a', href=True):
            link_text = link.text.lower().strip()
            if any(kw in link_text for kw in keywords) and len(link_text) > 5:
                href = link['href']
                if not href.startswith('http'):
                    href = self.url.rstrip('/') + '/' + href.lstrip('/')
                
                grant_id = f"{self.foundation_name}_{link_text[:50].replace(' ', '_')}"
                grants.append(GrantRecord(
                    grant_id=grant_id,
                    grant_source_url=href,
                    status=GrantStatus.SCOUTED,
                    extracted_requirements=[link_text.title()]
                ))
        
        return grants

class RSSFeedScraper(BaseScraper):
    """Parses RSS/XML feeds for grant opportunities (more reliable than HTML scraping)."""
    
    def __init__(self, feed_url: str, source_name: str):
        self.feed_url = feed_url
        self.source_name = source_name
    
    def scrape(self) -> List[GrantRecord]:
        try:
            response = requests.get(self.feed_url, timeout=15)
            if response.status_code != 200:
                print(f"Failed to fetch RSS feed {self.feed_url} (Status: {response.status_code})")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Network error fetching RSS feed {self.feed_url}: {e}")
            return []
        
        grants = []
        try:
            root = ET.fromstring(response.content)
            
            # Handle standard RSS format
            items = root.findall('.//item')
            if not items:
                # Try Atom format
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                items = root.findall('.//atom:entry', ns)
            
            for item in items[:20]:  # Cap at 20 per feed
                title = item.findtext('title', '') or item.findtext('{http://www.w3.org/2005/Atom}title', '')
                link = item.findtext('link', '') or ''
                
                # For Atom feeds, link is an attribute
                if not link:
                    link_elem = item.find('{http://www.w3.org/2005/Atom}link')
                    if link_elem is not None:
                        link = link_elem.get('href', '')
                
                if title and link:
                    grant_id = f"{self.source_name}_{title[:50].replace(' ', '_').replace('/', '_')}"
                    grants.append(GrantRecord(
                        grant_id=grant_id,
                        grant_source_url=link,
                        status=GrantStatus.SCOUTED,
                        extracted_requirements=[title]
                    ))
            
            print(f"  📰 Parsed {len(grants)} grants from {self.source_name} RSS feed")
        except ET.ParseError as e:
            print(f"⚠️ Could not parse RSS feed {self.feed_url}: {e}")
        
        return grants

class ScraperFactory:
    @staticmethod
    def get_scrapers() -> List[BaseScraper]:
        return [
            # RSS Feeds (most reliable - structured data, always online)
            RSSFeedScraper(
                "https://www.grants.gov/xml/XMLExtract.xml", 
                "GrantsGov"
            ),
            
            # Real foundation websites
            GenericScraper(
                "https://www.catholicextension.org/grants/", 
                "CatholicExtension"
            ),
            GenericScraper(
                "https://svdpusa.org/resources/", 
                "SVdPNational"
            ),
            GenericScraper(
                "https://www.rwjf.org/en/grants.html", 
                "RWJFoundation"
            ),
        ]

def _seed_demo_grants():
    """
    Seeds the database with sample grants so the UI is never empty.
    Only inserts if the grants table has zero rows.
    """
    from SvdpGrantAgent.factories.db_factory import get_db_connection
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM grants;")
        count = cur.fetchone()[0]
        if count == 0:
            print("Seeding database with demo grant opportunities...")
            demo_grants = [
                ("DEMO_community_food_bank_2026", "https://example.com/grants/food-bank", "Scouted"),
                ("DEMO_elderly_outreach_initiative", "https://example.com/grants/elderly-outreach", "Scouted"),
                ("DEMO_housing_assistance_fund", "https://example.com/grants/housing-assistance", "Scouted"),
            ]
            for grant_id, url, status in demo_grants:
                cur.execute("""
                    INSERT INTO grants (grant_id, grant_source_url, status)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (grant_id) DO NOTHING;
                """, (grant_id, url, status))
            conn.commit()
            print(f"✅ Seeded {len(demo_grants)} demo grants.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not seed demo grants: {e}")

def run_scout_job():
    from SvdpGrantAgent.factories.db_factory import get_db_connection
    import json
    
    scrapers = ScraperFactory.get_scrapers()
    all_grants = []
    for scraper in scrapers:
        name = getattr(scraper, 'foundation_name', None) or getattr(scraper, 'source_name', 'Unknown')
        print(f"Scraping {name}...")
        try:
            grants = scraper.scrape()
            all_grants.extend(grants)
        except Exception as e:
            print(f"⚠️ Scraper {name} failed: {e}")
    
    print(f"Found {len(all_grants)} potential grant opportunities. Saving to DB...")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for grant in all_grants:
            cur.execute("""
                INSERT INTO grants (grant_id, grant_source_url, status)
                VALUES (%s, %s, %s)
                ON CONFLICT (grant_id) DO NOTHING;
            """, (grant.grant_id, grant.grant_source_url, grant.status))
        
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not save scraped grants to DB: {e}")
    
    # If no live grants were found, seed the DB with demo grants so the UI isn't empty
    if len(all_grants) == 0:
        _seed_demo_grants()
        
    return all_grants


def run_discovery_job():
    """
    Runs the LLM-powered intelligent grant discovery.
    Searches the web and uses AI to evaluate grant eligibility for SVdP.
    """
    from SvdpGrantAgent.factories.db_factory import get_db_connection
    from SvdpGrantAgent.discovery import discover_grants
    
    discovered = discover_grants(max_queries=3)
    
    if not discovered:
        print("No qualifying grants found via AI discovery.")
        return discovered
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for grant in discovered:
            cur.execute("""
                INSERT INTO grants (grant_id, grant_source_url, status)
                VALUES (%s, %s, %s)
                ON CONFLICT (grant_id) DO NOTHING;
            """, (grant.grant_id, grant.grant_source_url, grant.status))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Saved {len(discovered)} AI-discovered grants to database.")
    except Exception as e:
        print(f"Warning: Could not save discovered grants to DB: {e}")
    
    return discovered


if __name__ == "__main__":
    run_scout_job()

