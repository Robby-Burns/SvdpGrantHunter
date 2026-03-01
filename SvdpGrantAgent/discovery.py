"""
Intelligent Grant Discovery Agent
Uses LLM to search the web and evaluate grant opportunities for SVdP St. Pats.
"""
import os
import requests
from typing import List, Optional
from bs4 import BeautifulSoup
from SvdpGrantAgent.schema import GrantRecord, GrantStatus
from SvdpGrantAgent.factories.llm_factory import get_llm_provider
from langchain_core.prompts import ChatPromptTemplate


# Search queries tailored to SVdP St. Pats mission areas
SVDP_SEARCH_QUERIES = [
    "community food bank grants Washington State 2026",
    "elderly outreach grants nonprofit Pacific Northwest",
    "housing assistance grants Catholic nonprofit",
    "poverty relief grants Tri-Cities Washington",
    "social services grants faith-based organizations",
    "emergency assistance grants low-income families Washington",
]

ELIGIBILITY_PROMPT = """You are a grant eligibility analyst for St. Vincent de Paul (St. Pats Conference), 
a Catholic nonprofit in the Tri-Cities area of Washington State.

Our mission areas:
- Food assistance (food banks, meal programs)
- Housing assistance (rent, utilities, emergency shelter)
- Elderly outreach (home visits, companionship, transportation)
- Poverty relief (financial assistance, job training referrals)

Given the following grant opportunity text scraped from a web page, determine:
1. Is this a REAL grant opportunity (not a news article, blog post, or unrelated page)?
2. Would SVdP St. Pats likely QUALIFY for this grant?
3. What is the grant about?

Respond in this exact format:
IS_GRANT: YES or NO
QUALIFIES: YES or NO  
GRANT_TITLE: (short title, max 60 chars)
REASON: (one sentence explanation)
"""


def _search_web_for_grants(query: str, num_results: int = 5) -> List[str]:
    """
    Uses a simple Google search scrape to find grant URLs.
    Falls back gracefully if blocked.
    """
    urls = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for result in soup.find_all('a', class_='result__a', limit=num_results):
                href = result.get('href', '')
                if href and href.startswith('http'):
                    urls.append(href)
    except Exception as e:
        print(f"⚠️ Web search failed for '{query}': {e}")
    
    return urls


def _extract_page_text(url: str, max_chars: int = 3000) -> Optional[str]:
    """
    Extracts readable text from a web page.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        text = soup.get_text(separator=' ', strip=True)
        return text[:max_chars] if text else None
    except Exception as e:
        print(f"⚠️ Could not extract text from {url}: {e}")
        return None


def _evaluate_grant_with_llm(page_text: str, source_url: str) -> Optional[GrantRecord]:
    """
    Uses the LLM to determine if page content is a real, qualifying grant.
    """
    try:
        llm = get_llm_provider(temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", ELIGIBILITY_PROMPT),
            ("human", "Grant page URL: {url}\n\nPage content:\n{content}")
        ])
        
        chain = prompt | llm
        response = chain.invoke({"url": source_url, "content": page_text})
        result = response.content
        
        # Parse the structured response
        is_grant = "IS_GRANT: YES" in result.upper()
        qualifies = "QUALIFIES: YES" in result.upper()
        
        # Extract grant title
        title_line = [l for l in result.split('\n') if 'GRANT_TITLE:' in l.upper()]
        grant_title = title_line[0].split(':', 1)[1].strip() if title_line else "Unknown Grant"
        
        if is_grant and qualifies:
            # Create a clean grant ID from the title
            grant_id = "DISC_" + grant_title[:40].replace(' ', '_').replace('/', '_')
            return GrantRecord(
                grant_id=grant_id,
                grant_source_url=source_url,
                status=GrantStatus.SCOUTED,
                extracted_requirements=[grant_title]
            )
        else:
            print(f"  ❌ Not qualifying: {source_url}")
            return None
            
    except Exception as e:
        print(f"⚠️ LLM evaluation failed for {source_url}: {e}")
        return None


def discover_grants(max_queries: int = 3) -> List[GrantRecord]:
    """
    Main discovery function. Searches the web, extracts content, 
    and uses LLM to evaluate grant eligibility.
    """
    print("🔍 Starting intelligent grant discovery...")
    discovered = []
    seen_urls = set()
    
    for query in SVDP_SEARCH_QUERIES[:max_queries]:
        print(f"\n🔎 Searching: '{query}'")
        urls = _search_web_for_grants(query)
        print(f"  Found {len(urls)} potential pages")
        
        for url in urls:
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            print(f"  📄 Evaluating: {url[:80]}...")
            page_text = _extract_page_text(url)
            if not page_text or len(page_text) < 100:
                continue
            
            grant = _evaluate_grant_with_llm(page_text, url)
            if grant:
                print(f"  ✅ FOUND: {grant.grant_id}")
                discovered.append(grant)
    
    print(f"\n🎯 Discovery complete. Found {len(discovered)} qualifying grants.")
    return discovered
