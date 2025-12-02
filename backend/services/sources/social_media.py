"""
Social Media Search Service
Searches Facebook, Twitter, Instagram, LinkedIn, GitHub, Reddit, etc.
"""

import logging
from typing import Dict, Any, List
import aiohttp
from bs4 import BeautifulSoup
import asyncio
import re

logger = logging.getLogger(__name__)


class SocialMediaService:
    """Social media platform search integration"""
    
    def __init__(self):
        self.platforms = {
            'facebook': 'facebook.com',
            'twitter': 'twitter.com',
            'instagram': 'instagram.com',
            'linkedin': 'linkedin.com',
            'github': 'github.com',
            'reddit': 'reddit.com',
            'tiktok': 'tiktok.com',
            'youtube': 'youtube.com'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def search_all_platforms(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Search across all social media platforms"""
        try:
            tasks = [
                self._search_facebook(query),
                self._search_twitter(query),
                self._search_instagram(query),
                self._search_linkedin(query),
                self._search_github(query),
                self._search_reddit(query)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                'facebook': results[0] if not isinstance(results[0], Exception) else {'error': str(results[0])},
                'twitter': results[1] if not isinstance(results[1], Exception) else {'error': str(results[1])},
                'instagram': results[2] if not isinstance(results[2], Exception) else {'error': str(results[2])},
                'linkedin': results[3] if not isinstance(results[3], Exception) else {'error': str(results[3])},
                'github': results[4] if not isinstance(results[4], Exception) else {'error': str(results[4])},
                'reddit': results[5] if not isinstance(results[5], Exception) else {'error': str(results[5])}
            }
        
        except Exception as e:
            logger.error(f"Social media search error: {str(e)}")
            return {'error': str(e)}
    
    async def _search_facebook(self, query: Dict) -> Dict:
        """Search Facebook using Google dorking"""
        search_term = query.get('name') or query.get('username') or query.get('email')
        if not search_term:
            return {'profiles': []}
        
        # Use Google to search Facebook
        google_query = f'site:facebook.com "{search_term}"'
        # Implementation would use Google Custom Search API
        return {'profiles': [], 'platform': 'facebook'}
    
    async def _search_twitter(self, query: Dict) -> Dict:
        """Search Twitter/X profiles"""
        username = query.get('username') or self._extract_username(query.get('name', ''))
        profiles = []
        
        if username:
            url = f"https://twitter.com/{username}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.headers, timeout=10) as response:
                        if response.status == 200:
                            profiles.append({
                                'platform': 'twitter',
                                'username': username,
                                'url': url,
                                'exists': True
                            })
            except:
                pass
        
        return {'profiles': profiles, 'platform': 'twitter'}
    
    async def _search_instagram(self, query: Dict) -> Dict:
        """Search Instagram profiles"""
        username = query.get('username') or self._extract_username(query.get('name', ''))
        profiles = []
        
        if username:
            url = f"https://www.instagram.com/{username}/"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.headers, timeout=10) as response:
                        if response.status == 200:
                            profiles.append({
                                'platform': 'instagram',
                                'username': username,
                                'url': url,
                                'exists': True
                            })
            except:
                pass
        
        return {'profiles': profiles, 'platform': 'instagram'}
    
    async def _search_linkedin(self, query: Dict) -> Dict:
        """Search LinkedIn profiles"""
        # LinkedIn requires authentication for most searches
        # Would use Google dorking: site:linkedin.com/in/ "name"
        return {'profiles': [], 'platform': 'linkedin'}
    
    async def _search_github(self, query: Dict) -> Dict:
        """Search GitHub profiles"""
        username = query.get('username') or query.get('email')
        if not username:
            return {'profiles': [], 'platform': 'github'}
        
        try:
            url = f"https://api.github.com/search/users?q={username}"
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'},
                    timeout=10
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        profiles = [{
                            'platform': 'github',
                            'username': user['login'],
                            'url': user['html_url'],
                            'avatar': user['avatar_url']
                        } for user in data.get('items', [])]
                        return {'profiles': profiles, 'platform': 'github'}
        except Exception as e:
            logger.error(f"GitHub search error: {str(e)}")
        
        return {'profiles': [], 'platform': 'github'}
    
    async def _search_reddit(self, query: Dict) -> Dict:
        """Search Reddit profiles"""
        username = query.get('username') or self._extract_username(query.get('name', ''))
        if not username:
            return {'profiles': [], 'platform': 'reddit'}
        
        try:
            url = f"https://www.reddit.com/user/{username}/about.json"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        user_data = data.get('data', {})
                        return {
                            'profiles': [{
                                'platform': 'reddit',
                                'username': user_data.get('name'),
                                'url': f"https://www.reddit.com/user/{user_data.get('name')}",
                                'karma': user_data.get('total_karma'),
                                'created': user_data.get('created_utc')
                            }],
                            'platform': 'reddit'
                        }
        except Exception as e:
            logger.error(f"Reddit search error: {str(e)}")
        
        return {'profiles': [], 'platform': 'reddit'}
    
    def _extract_username(self, name: str) -> str:
        """Extract potential username from name"""
        if not name:
            return ''
        return re.sub(r'[^a-z0-9_]', '', name.lower().replace(' ', ''))
    
    async def check_username_across_platforms(self, username: str) -> Dict[str, Dict]:
        """Check if username exists across all platforms"""
        results = {}
        
        for platform, domain in self.platforms.items():
            url = self._build_profile_url(platform, username)
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.head(url, headers=self.headers, timeout=5, allow_redirects=True) as response:
                        results[platform] = {
                            'exists': response.status == 200,
                            'url': url
                        }
            except:
                results[platform] = {'exists': False, 'url': url}
        
        return results
    
    def _build_profile_url(self, platform: str, username: str) -> str:
        """Build profile URL for platform"""
        urls = {
            'facebook': f"https://facebook.com/{username}",
            'twitter': f"https://twitter.com/{username}",
            'instagram': f"https://instagram.com/{username}",
            'linkedin': f"https://linkedin.com/in/{username}",
            'github': f"https://github.com/{username}",
            'reddit': f"https://reddit.com/user/{username}",
            'tiktok': f"https://tiktok.com/@{username}",
            'youtube': f"https://youtube.com/@{username}"
        }
        return urls.get(platform, '')
