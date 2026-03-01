import requests
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
        Simple generic scraper. In production, this would be highly customized 
        or use an LLM for DOM parsing.
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
        
        # Placeholder logic for finding "grants" - highly dependent on site structure
        grants = []
        
        # Example: look for links containing "grant" or "funding"
        for link in soup.find_all('a', href=True):
            if 'grant' in link.text.lower() or 'funding' in link.text.lower():
                grant_id = f"{self.foundation_name}_{link['href'].split('/')[-1]}"
                grants.append(GrantRecord(
                    grant_id=grant_id,
                    grant_source_url=link['href'] if link['href'].startswith('http') else self.url + link['href'],
                    status=GrantStatus.SCOUTED
                ))
        
        return grants

class ScraperFactory:
    @staticmethod
    def get_scrapers() -> List[BaseScraper]:
        return [
            GenericScraper("https://3riverscf.org/grants/", "3Rivers"),
            GenericScraper("https://www.catholicfoundation.org/grants", "CatholicFoundation")
        ]

def run_scout_job():
    from SvdpGrantAgent.factories.db_factory import get_db_connection
    import json
    
    scrapers = ScraperFactory.get_scrapers()
    all_grants = []
    for scraper in scrapers:
        print(f"Scraping {scraper.foundation_name}...")
        grants = scraper.scrape()
        all_grants.extend(grants)
    
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
        
    return all_grants

if __name__ == "__main__":
    run_scout_job()
