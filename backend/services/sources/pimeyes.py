"""
PimEyes reverse face search service
"""

import os
import base64
import logging
from typing import Dict, Any, Optional, List
import aiohttp
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class PimEyesService:
    """PimEyes reverse face search - web scraping approach"""
    
    def __init__(self):
        self.base_url = "https://pimeyes.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def search_by_image(self, image: str) -> Dict[str, Any]:
        """
        Search by image using PimEyes web interface (scraping)
        Note: This is a placeholder - actual implementation would require
        reverse engineering PimEyes' web interface or using alternatives
        
        Args:
            image: Base64 encoded image, image URL, or file path
            
        Returns:
            Search results with potential matches
        """
        try:
            logger.warning("PimEyes requires API access or manual search - returning placeholder")
            return {
                'matches': [],
                'source': 'pimeyes',
                'note': 'PimEyes requires API subscription or manual search via website',
                'suggestion': 'Use Google Images reverse search or TinEye as free alternatives'
            }
        
        except Exception as e:
            logger.error(f"PimEyes search error: {str(e)}")
            return {'error': str(e), 'matches': []}
    
    def _parse_results(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and normalize PimEyes results"""
        if not data or 'results' not in data:
            return {'matches': []}
        
        matches = []
        for result in data.get('results', []):
            match = {
                'url': result.get('url'),
                'thumbnail': result.get('thumbnail_url'),
                'score': result.get('score', 0),
                'source': result.get('source'),
                'title': result.get('title', ''),
                'snippet': result.get('snippet', ''),
                'metadata': {
                    'domain': urlparse(result.get('url', '')).hostname if result.get('url') else None,
                    'possible_names': self._extract_names(result.get('title', ''), result.get('snippet', '')),
                    'possible_locations': self._extract_locations(result.get('title', ''), result.get('snippet', ''))
                }
            }
            matches.append(match)
        
        return {
            'matches': matches,
            'total_results': data.get('total_results', len(matches)),
            'source': 'pimeyes'
        }
    
    def _extract_names(self, title: str, snippet: str) -> list:
        """Extract potential names using regex"""
        text = f"{title} {snippet}"
        # Pattern for capitalized names (First Last or First Middle Last)
        pattern = r'\b([A-Z][a-z]+ [A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\b'
        matches = re.findall(pattern, text)
        return list(set(matches))  # Remove duplicates
    
    def _extract_locations(self, title: str, snippet: str) -> list:
        """Extract potential locations"""
        text = f"{title} {snippet}"
        # Simple location pattern: City, ST
        pattern = r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)?),\s*([A-Z]{2})\b'
        matches = re.findall(pattern, text)
        return [f"{city}, {state}" for city, state in matches]
