"""
FastPeopleSearch scraper service
Public records and people search aggregator
"""

import logging
from typing import Dict, Any, List
import aiohttp
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class FastPeopleSearchService:
    """FastPeopleSearch integration for public records"""
    
    def __init__(self):
        self.base_url = "https://www.fastpeoplesearch.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def search(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for person by various identifiers
        
        Args:
            query: Can contain name, phone, address, email, location
            
        Returns:
            Person data including address, phone, relatives
        """
        try:
            results = []
            
            # Search by name
            if query.get('name'):
                name_results = await self._search_by_name(
                    query['name'],
                    query.get('location', '')
                )
                results.extend(name_results)
            
            # Search by phone
            if query.get('phone'):
                phone_results = await self._search_by_phone(query['phone'])
                results.extend(phone_results)
            
            # Search by address
            if query.get('address'):
                address_results = await self._search_by_address(query['address'])
                results.extend(address_results)
            
            return {
                'source': 'FastPeopleSearch',
                'results': self._deduplicate(results)
            }
        
        except Exception as e:
            logger.error(f"FastPeopleSearch error: {str(e)}")
            return {'source': 'FastPeopleSearch', 'error': str(e), 'results': []}
    
    async def _search_by_name(self, name: str, location: str = '') -> List[Dict]:
        """Search by person name"""
        try:
            parts = name.strip().split()
            if len(parts) < 2:
                return []
            
            first_name = parts[0]
            last_name = ' '.join(parts[1:])
            
            # Build URL
            url_path = f"/name/{first_name}-{last_name}"
            if location:
                url_path += f"_{location.replace(' ', '-').replace(',', '')}"
            
            url = f"{self.base_url}{url_path}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=15) as response:
                    if response.status != 200:
                        return []
                    
                    html = await response.text()
                    return self._parse_results(html)
        
        except Exception as e:
            logger.error(f"Name search error: {str(e)}")
            return []
    
    async def _search_by_phone(self, phone: str) -> List[Dict]:
        """Search by phone number"""
        try:
            clean_phone = re.sub(r'\D', '', phone)
            url = f"{self.base_url}/phone/{clean_phone}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=15) as response:
                    if response.status != 200:
                        return []
                    
                    html = await response.text()
                    return self._parse_results(html)
        
        except Exception as e:
            logger.error(f"Phone search error: {str(e)}")
            return []
    
    async def _search_by_address(self, address: str) -> List[Dict]:
        """Search by address"""
        try:
            formatted_address = address.replace(' ', '-').replace(',', '')
            url = f"{self.base_url}/address/{formatted_address}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=15) as response:
                    if response.status != 200:
                        return []
                    
                    html = await response.text()
                    return self._parse_results(html)
        
        except Exception as e:
            logger.error(f"Address search error: {str(e)}")
            return []
    
    def _parse_results(self, html: str) -> List[Dict]:
        """Parse HTML results from FastPeopleSearch"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # Find all person cards
        cards = soup.find_all('div', class_='card')
        
        for card in cards:
            person = {
                'name': self._get_text(card, '.card-title, .name'),
                'age': self._extract_age(self._get_text(card, '.age, .birth-info')),
                'addresses': [],
                'phones': [],
                'relatives': [],
                'associates': [],
                'emails': []
            }
            
            # Extract addresses
            for addr_elem in card.find_all(class_=['address-line', 'address', 'location']):
                address_text = addr_elem.get_text(strip=True)
                if address_text:
                    person['addresses'].append({
                        'full': address_text,
                        'type': 'current' if 'current' in addr_elem.get('class', []) else 'previous'
                    })
            
            # Extract phone numbers
            for phone_elem in card.find_all(class_=['phone', 'phone-number']):
                phone_text = phone_elem.get_text(strip=True)
                if phone_text:
                    person['phones'].append({
                        'number': phone_text,
                        'type': self._detect_phone_type(phone_elem.get('class', []))
                    })
            
            # Extract relatives
            for rel_elem in card.find_all(class_=['relative', 'family-member']):
                relative = rel_elem.get_text(strip=True)
                if relative:
                    person['relatives'].append({
                        'name': relative,
                        'relationship': 'possible relative'
                    })
            
            # Extract associates
            for assoc_elem in card.find_all(class_=['associate', 'known-associate']):
                associate = assoc_elem.get_text(strip=True)
                if associate:
                    person['associates'].append(associate)
            
            # Extract emails
            for email_elem in card.find_all(class_=['email', 'email-address']):
                email = email_elem.get_text(strip=True)
                if email and '@' in email:
                    person['emails'].append(email)
            
            if person['name']:
                results.append(person)
        
        return results
    
    def _get_text(self, element, selector: str) -> str:
        """Safely get text from element using CSS selector"""
        found = element.select_one(selector)
        return found.get_text(strip=True) if found else ''
    
    def _extract_age(self, text: str) -> str:
        """Extract age from text"""
        match = re.search(r'\d+', text)
        return match.group(0) if match else ''
    
    def _detect_phone_type(self, classes: List[str]) -> str:
        """Detect phone type from CSS classes"""
        class_str = ' '.join(classes).lower()
        if 'mobile' in class_str:
            return 'mobile'
        elif 'landline' in class_str:
            return 'landline'
        elif 'voip' in class_str:
            return 'voip'
        return 'unknown'
    
    def _deduplicate(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate results"""
        seen = set()
        unique = []
        
        for result in results:
            key = f"{result.get('name', '')}-{result.get('age', '')}"
            if key not in seen:
                seen.add(key)
                unique.append(result)
        
        return unique
