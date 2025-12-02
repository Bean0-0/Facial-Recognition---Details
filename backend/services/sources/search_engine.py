"""
Search Engine Service - Google and Bing with advanced operators
"""

import os
import logging
from typing import Dict, Any, List
import aiohttp
from bs4 import BeautifulSoup
import asyncio

logger = logging.getLogger(__name__)


class SearchEngineService:
    """Search engine integration using web scraping (no API keys required)"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def comprehensive_search(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive searches across Google and Bing"""
        try:
            searches = []
            
            if query.get('name'):
                searches.append(self._search_person(query['name'], query.get('location', '')))
            if query.get('email'):
                searches.append(self._search_email(query['email']))
            if query.get('username'):
                searches.append(self._search_username(query['username']))
            if query.get('phone'):
                searches.append(self._search_phone(query['phone']))
            
            results = await asyncio.gather(*searches, return_exceptions=True)
            
            return {
                'google': [r for r in results if not isinstance(r, Exception)],
                'timestamp': None
            }
        
        except Exception as e:
            logger.error(f"Search engine error: {str(e)}")
            return {'error': str(e), 'results': []}
    
    async def _search_person(self, name: str, location: str = '') -> Dict:
        """Search for person with advanced operators"""
        queries = [
            f'"{name}"',
            f'"{name}" {location}' if location else None,
            f'site:linkedin.com "{name}"',
            f'site:facebook.com "{name}"',
            f'"{name}" (contact OR email OR phone)',
        ]
        queries = [q for q in queries if q]
        
        results = await asyncio.gather(*[self._google_search(q) for q in queries], return_exceptions=True)
        
        return {
            'type': 'person',
            'query': name,
            'results': [r for r in results if not isinstance(r, Exception)]
        }
    
    async def _search_email(self, email: str) -> Dict:
        """Search for email address"""
        domain = email.split('@')[1] if '@' in email else ''
        queries = [
            f'"{email}"',
            f'"{email}" -site:{domain}' if domain else None,
            f'filetype:pdf "{email}"',
        ]
        queries = [q for q in queries if q]
        
        results = await asyncio.gather(*[self._google_search(q) for q in queries], return_exceptions=True)
        
        return {
            'type': 'email',
            'query': email,
            'results': [r for r in results if not isinstance(r, Exception)]
        }
    
    async def _search_username(self, username: str) -> Dict:
        """Search for username across platforms"""
        platforms = ['facebook', 'twitter', 'instagram', 'linkedin', 'github', 'reddit']
        queries = [f'site:{platform}.com "{username}"' for platform in platforms]
        
        results = await asyncio.gather(*[self._google_search(q) for q in queries], return_exceptions=True)
        
        return {
            'type': 'username',
            'query': username,
            'results': [r for r in results if not isinstance(r, Exception)]
        }
    
    async def _search_phone(self, phone: str) -> Dict:
        """Search for phone number"""
        queries = [f'"{phone}"', f'"{phone}" (contact OR profile)']
        
        results = await asyncio.gather(*[self._google_search(q) for q in queries], return_exceptions=True)
        
        return {
            'type': 'phone',
            'query': phone,
            'results': [r for r in results if not isinstance(r, Exception)]
        }
    
    async def _google_search(self, query: str, num: int = 10) -> List[Dict]:
        """Execute Google search by scraping results page"""
        try:
            url = f'https://www.google.com/search?q={query}&num={num}'
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=10) as response:
                    if response.status != 200:
                        logger.warning(f"Google search returned status {response.status}")
                        return []
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    # Parse Google search results
                    for g in soup.find_all('div', class_='g'):
                        title_elem = g.find('h3')
                        link_elem = g.find('a')
                        snippet_elem = g.find('div', class_=['VwiC3b', 'IsZvec'])
                        
                        if title_elem and link_elem:
                            results.append({
                                'title': title_elem.get_text(),
                                'url': link_elem.get('href', ''),
                                'snippet': snippet_elem.get_text() if snippet_elem else '',
                                'display_url': link_elem.get('href', '').split('/')[2] if '/' in link_elem.get('href', '') else ''
                            })
                    
                    return results
        
        except Exception as e:
            logger.error(f"Google search error: {str(e)}")
            return []
    
    async def _bing_search(self, query: str, num: int = 10) -> List[Dict]:
        """Execute Bing search by scraping results page"""
        try:
            url = f'https://www.bing.com/search?q={query}&count={num}'
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=10) as response:
                    if response.status != 200:
                        return []
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    # Parse Bing search results
                    for result in soup.find_all('li', class_='b_algo'):
                        title_elem = result.find('h2')
                        link_elem = result.find('a')
                        snippet_elem = result.find('p')
                        
                        if title_elem and link_elem:
                            results.append({
                                'title': title_elem.get_text(),
                                'url': link_elem.get('href', ''),
                                'snippet': snippet_elem.get_text() if snippet_elem else '',
                                'display_url': link_elem.get('href', '').split('/')[2] if '/' in link_elem.get('href', '') else ''
                            })
                    
                    return results
        
        except Exception as e:
            logger.error(f"Bing search error: {str(e)}")
            return []
