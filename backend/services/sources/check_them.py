"""CheckThem people search service"""

import logging
from typing import Dict, Any, List
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class CheckThemService:
    def __init__(self):
        self.base_url = "https://checkthem.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def search(self, query: Dict[str, Any]) -> Dict[str, Any]:
        try:
            results = []
            
            if query.get('name'):
                results.extend(await self._search_by_name(query['name'], query.get('location', '')))
            if query.get('phone'):
                results.extend(await self._search_by_phone(query['phone']))
            if query.get('email'):
                results.extend(await self._search_by_email(query['email']))
            
            return {'source': 'CheckThem', 'results': self._deduplicate(results)}
        except Exception as e:
            logger.error(f"CheckThem error: {str(e)}")
            return {'source': 'CheckThem', 'error': str(e), 'results': []}
    
    async def _search_by_name(self, name: str, location: str = '') -> List[Dict]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/search",
                    json={'name': name, 'location': location},
                    headers=self.headers,
                    timeout=15
                ) as response:
                    if response.status != 200:
                        return []
                    data = await response.json() if response.content_type == 'application/json' else await response.text()
                    return self._parse_results(data)
        except Exception as e:
            logger.error(f"CheckThem name search error: {str(e)}")
            return []
    
    async def _search_by_phone(self, phone: str) -> List[Dict]:
        return []
    
    async def _search_by_email(self, email: str) -> List[Dict]:
        return []
    
    def _parse_results(self, data) -> List[Dict]:
        if isinstance(data, str):
            return self._parse_html(data)
        return data.get('results', []) if isinstance(data, dict) else []
    
    def _parse_html(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        return []
    
    def _deduplicate(self, results: List[Dict]) -> List[Dict]:
        seen = set()
        return [r for r in results if not (
            (key := f"{r.get('name', '')}-{r.get('age', '')}") in seen or seen.add(key)
        )]
