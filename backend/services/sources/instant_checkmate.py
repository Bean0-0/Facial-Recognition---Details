"""Instant Checkmate people search service"""

import logging
from typing import Dict, Any, List
import aiohttp
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class InstantCheckmateService:
    def __init__(self):
        self.base_url = "https://www.instantcheckmate.com"
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
            
            return {'source': 'InstantCheckmate', 'results': self._deduplicate(results)}
        except Exception as e:
            logger.error(f"InstantCheckmate error: {str(e)}")
            return {'source': 'InstantCheckmate', 'error': str(e), 'results': []}
    
    async def _search_by_name(self, name: str, location: str = '') -> List[Dict]:
        return []
    
    async def _search_by_phone(self, phone: str) -> List[Dict]:
        return []
    
    def _deduplicate(self, results: List[Dict]) -> List[Dict]:
        seen = set()
        return [r for r in results if not (
            (key := f"{r.get('name', '')}-{r.get('age', '')}") in seen or seen.add(key)
        )]
