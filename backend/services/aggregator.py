"""
Main data aggregation service
Coordinates searches across all sources and uses LLM for correlation
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

from .sources.pimeyes import PimEyesService
from .sources.facecheck import FaceCheckService
from .sources.fast_people_search import FastPeopleSearchService
from .sources.check_them import CheckThemService
from .sources.instant_checkmate import InstantCheckmateService
from .sources.search_engine import SearchEngineService
from .sources.social_media import SocialMediaService
from .llm_processor import LLMProcessor

logger = logging.getLogger(__name__)


class PeopleDataAggregator:
    """Main aggregator coordinating all data sources"""
    
    def __init__(self):
        self.sources = {
            'pimeyes': PimEyesService(),
            'facecheck': FaceCheckService(),
            'fastpeoplesearch': FastPeopleSearchService(),
            'checkthem': CheckThemService(),
            'instantcheckmate': InstantCheckmateService(),
            'searchengine': SearchEngineService(),
            'socialmedia': SocialMediaService()
        }
        self.llm = LLMProcessor()
    
    async def aggregate_person_data(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main aggregation function - performs comprehensive person search
        
        Args:
            query: Search parameters (name, image, email, phone, username, address, location)
            
        Returns:
            Aggregated results from all sources with LLM-based consolidation
        """
        search_id = str(uuid.uuid4())
        logger.info(f"Starting aggregation search {search_id} with query: {query}")
        
        results = {
            'search_id': search_id,
            'timestamp': datetime.utcnow().isoformat(),
            'sources': {},
            'consolidated': None
        }
        
        try:
            # Phase 1: Reverse face search (if image provided)
            if 'image' in query:
                logger.info("Phase 1: Running reverse face search...")
                face_results = await self._run_face_search(query['image'])
                results['sources']['pimeyes'] = face_results.get('pimeyes')
                results['sources']['facecheck'] = face_results.get('facecheck')
                
                # Extract names from face search results using LLM
                if not query.get('name'):
                    extracted_names = await self.llm.extract_names_from_face_search(face_results)
                    if extracted_names:
                        query['name'] = extracted_names[0]
                        logger.info(f"Extracted name from face search: {query['name']}")
            
            # Phase 2: People aggregator searches
            if any(k in query for k in ['name', 'phone', 'email', 'address']):
                logger.info("Phase 2: Running people aggregator searches...")
                people_results = await self._run_people_searches(query)
                results['sources'].update(people_results)
            
            # Phase 3: Search engine queries
            if any(k in query for k in ['name', 'email', 'username']):
                logger.info("Phase 3: Running search engine queries...")
                search_results = await self._run_search_engine(query)
                results['sources']['searchengine'] = search_results
            
            # Phase 4: Social media searches
            if any(k in query for k in ['name', 'username', 'email']):
                logger.info("Phase 4: Running social media searches...")
                social_results = await self._run_social_media(query)
                results['sources']['socialmedia'] = social_results
            
            # Phase 5: LLM-powered consolidation
            logger.info("Phase 5: Consolidating data with LLM...")
            results['consolidated'] = await self.llm.consolidate_person_data(results['sources'])
            
            logger.info(f"Aggregation search {search_id} completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in aggregation search {search_id}: {str(e)}", exc_info=True)
            results['error'] = str(e)
            return results
    
    async def _run_face_search(self, image: str) -> Dict[str, Any]:
        """Run reverse face searches in parallel"""
        tasks = [
            self.sources['pimeyes'].search_by_image(image),
            self.sources['facecheck'].search_by_image(image)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            'pimeyes': results[0] if not isinstance(results[0], Exception) else {'error': str(results[0])},
            'facecheck': results[1] if not isinstance(results[1], Exception) else {'error': str(results[1])}
        }
    
    async def _run_people_searches(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Run people aggregator searches in parallel"""
        tasks = [
            self.sources['fastpeoplesearch'].search(query),
            self.sources['checkthem'].search(query),
            self.sources['instantcheckmate'].search(query)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            'fastpeoplesearch': results[0] if not isinstance(results[0], Exception) else {'error': str(results[0])},
            'checkthem': results[1] if not isinstance(results[1], Exception) else {'error': str(results[1])},
            'instantcheckmate': results[2] if not isinstance(results[2], Exception) else {'error': str(results[2])}
        }
    
    async def _run_search_engine(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Run search engine queries"""
        try:
            return await self.sources['searchengine'].comprehensive_search(query)
        except Exception as e:
            logger.error(f"Search engine error: {str(e)}")
            return {'error': str(e)}
    
    async def _run_social_media(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Run social media searches"""
        try:
            return await self.sources['socialmedia'].search_all_platforms(query)
        except Exception as e:
            logger.error(f"Social media error: {str(e)}")
            return {'error': str(e)}
    
    async def search_source(self, source_name: str, query: Dict[str, Any]) -> Any:
        """Search a specific source by name"""
        if source_name not in self.sources:
            raise ValueError(f"Unknown source: {source_name}")
        
        source = self.sources[source_name]
        
        # Handle different search methods
        if hasattr(source, 'search'):
            return await source.search(query)
        elif hasattr(source, 'search_by_image') and 'image' in query:
            return await source.search_by_image(query['image'])
        elif hasattr(source, 'comprehensive_search'):
            return await source.comprehensive_search(query)
        elif hasattr(source, 'search_all_platforms'):
            return await source.search_all_platforms(query)
        else:
            raise ValueError(f"Source {source_name} does not support search operation")
    
    def get_available_sources(self) -> List[str]:
        """Get list of available source names"""
        return list(self.sources.keys())
