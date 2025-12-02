"""
LLM Processor Service
Uses OpenAI/Anthropic to extract names, correlate data, and consolidate information
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
import asyncio

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)


class LLMProcessor:
    """LLM-powered data processing and correlation"""
    
    def __init__(self):
        self.provider = os.getenv('LLM_PROVIDER', 'gemini').lower()
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        
        if self.provider == 'gemini' and GEMINI_AVAILABLE and self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.client = genai.GenerativeModel('gemini-1.5-flash')
            self.model = 'gemini-1.5-flash'
            logger.info(f"LLM initialized with Google Gemini ({self.model})")
        elif self.provider == 'openai' and OPENAI_AVAILABLE and self.openai_key:
            self.client = AsyncOpenAI(api_key=self.openai_key)
            self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
            logger.info(f"LLM initialized with OpenAI ({self.model})")
        elif self.provider == 'anthropic' and ANTHROPIC_AVAILABLE and self.anthropic_key:
            self.client = AsyncAnthropic(api_key=self.anthropic_key)
            self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')
            logger.info(f"LLM initialized with Anthropic ({self.model})")
        else:
            self.client = None
            logger.warning("No LLM configured - name extraction and consolidation will be limited")
    
    def is_configured(self) -> bool:
        """Check if LLM is properly configured"""
        return self.client is not None
    
    async def extract_names_from_face_search(self, face_results: Dict[str, Any]) -> List[str]:
        """
        Extract person names from reverse face search results
        
        Args:
            face_results: Results from PimEyes and FaceCheck searches
            
        Returns:
            List of extracted names, ordered by confidence
        """
        if not self.is_configured():
            # Fallback: simple regex extraction
            return self._extract_names_regex(face_results)
        
        try:
            prompt = self._build_name_extraction_prompt(face_results)
            
            if self.provider == 'gemini':
                # Gemini API call
                response = await asyncio.to_thread(
                    self.client.generate_content,
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3
                    )
                )
                # Parse JSON from response
                text = response.text.strip()
                if text.startswith('```json'):
                    text = text.split('```json')[1].split('```')[0].strip()
                elif text.startswith('```'):
                    text = text.split('```')[1].split('```')[0].strip()
                result = json.loads(text)
                
            elif self.provider == 'openai':
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert at extracting person names from web search results. Return only the most likely full names as a JSON array."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                result = json.loads(response.choices[0].message.content)
                
            elif self.provider == 'anthropic':
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                result = json.loads(response.content[0].text)
            
            return result.get('names', [])
            
        except Exception as e:
            logger.error(f"LLM name extraction error: {str(e)}")
            return self._extract_names_regex(face_results)
    
    async def extract_names(self, text: str) -> List[str]:
        """Extract person names from arbitrary text"""
        if not self.is_configured():
            return self._extract_names_regex({'text': text})
        
        try:
            prompt = f"""Extract all person names from the following text. Return them as a JSON array.
            
Text: {text}

Return format: {{"names": ["Name 1", "Name 2", ...]}}"""
            
            if self.provider == 'gemini':
                response = await asyncio.to_thread(
                    self.client.generate_content,
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3
                    )
                )
                text_response = response.text.strip()
                if text_response.startswith('```json'):
                    text_response = text_response.split('```json')[1].split('```')[0].strip()
                elif text_response.startswith('```'):
                    text_response = text_response.split('```')[1].split('```')[0].strip()
                result = json.loads(text_response)
                
            elif self.provider == 'openai':
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert at extracting person names from text."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                result = json.loads(response.choices[0].message.content)
                
            elif self.provider == 'anthropic':
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                result = json.loads(response.content[0].text)
            
            return result.get('names', [])
            
        except Exception as e:
            logger.error(f"LLM text extraction error: {str(e)}")
            return []
    
    async def consolidate_person_data(self, sources: Dict[str, Any]) -> Dict[str, Any]:
        """
        Consolidate data from multiple sources into a unified person profile
        Uses LLM to infer relationships and resolve conflicts
        
        Args:
            sources: Dict containing results from all data sources
            
        Returns:
            Consolidated person profile with high-confidence data
        """
        if not self.is_configured():
            logger.warning("LLM not configured - using basic consolidation")
            return self._basic_consolidation(sources)
        
        try:
            prompt = self._build_consolidation_prompt(sources)
            
            if self.provider == 'gemini':
                response = await asyncio.to_thread(
                    self.client.generate_content,
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.2
                    )
                )
                text_response = response.text.strip()
                if text_response.startswith('```json'):
                    text_response = text_response.split('```json')[1].split('```')[0].strip()
                elif text_response.startswith('```'):
                    text_response = text_response.split('```')[1].split('```')[0].strip()
                result = json.loads(text_response)
                
            elif self.provider == 'openai':
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": """You are an expert data analyst specializing in consolidating person information from multiple sources. 
                        Your task is to:
                        1. Identify the most reliable information from each source
                        2. Resolve conflicts between sources
                        3. Infer relationships between different data points
                        4. Build a comprehensive person profile
                        5. Include confidence scores for each field
                        
                        Return the consolidated profile as structured JSON."""},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                result = json.loads(response.choices[0].message.content)
                
            elif self.provider == 'anthropic':
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                result = json.loads(response.content[0].text)
            
            return result
            
        except Exception as e:
            logger.error(f"LLM consolidation error: {str(e)}")
            return self._basic_consolidation(sources)
    
    def _build_name_extraction_prompt(self, face_results: Dict[str, Any]) -> str:
        """Build prompt for name extraction from face search results"""
        prompt = """Analyze the following reverse face search results and extract the most likely person names.
        Look for names in titles, snippets, and URLs. Return the top 5 most confident names.
        
Face Search Results:
"""
        prompt += json.dumps(face_results, indent=2)
        prompt += '\n\nReturn format: {"names": ["Full Name 1", "Full Name 2", ...]}'
        
        return prompt
    
    def _build_consolidation_prompt(self, sources: Dict[str, Any]) -> str:
        """Build prompt for data consolidation"""
        prompt = """Consolidate the following person data from multiple sources into a single, comprehensive profile.

Data Sources:
"""
        prompt += json.dumps(sources, indent=2)
        
        prompt += """

Create a consolidated profile with the following structure:
{
  "person": {
    "name": "Full Name",
    "confidence": 0.0-1.0,
    "age": "age or age range",
    "current_location": {
      "city": "City",
      "state": "State",
      "address": "Full Address if available"
    }
  },
  "contact": {
    "phones": [{"number": "...", "type": "mobile/landline", "confidence": 0.0-1.0}],
    "emails": ["email@example.com"],
    "addresses": [{"full": "...", "type": "current/previous", "confidence": 0.0-1.0}]
  },
  "relationships": {
    "relatives": [{"name": "...", "relationship": "..."}],
    "associates": ["name"]
  },
  "online_presence": {
    "social_media": [{"platform": "...", "url": "...", "username": "..."}],
    "websites": ["url"],
    "profiles": ["url"]
  },
  "background": {
    "criminal_records": true/false,
    "court_records": true/false,
    "business_records": ["..."]
  },
  "metadata": {
    "sources_used": ["source1", "source2"],
    "data_quality": "high/medium/low",
    "last_updated": "timestamp"
  }
}

Resolve any conflicts between sources and include confidence scores."""
        
        return prompt
    
    def _extract_names_regex(self, data: Any) -> List[str]:
        """Fallback regex-based name extraction"""
        import re
        
        text = json.dumps(data)
        # Simple pattern for capitalized names
        pattern = r'\b([A-Z][a-z]+ [A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\b'
        matches = re.findall(pattern, text)
        
        # Deduplicate and return
        return list(dict.fromkeys(matches))[:5]
    
    def _basic_consolidation(self, sources: Dict[str, Any]) -> Dict[str, Any]:
        """Basic consolidation without LLM"""
        consolidated = {
            "person": {},
            "contact": {"phones": [], "emails": [], "addresses": []},
            "relationships": {"relatives": [], "associates": []},
            "online_presence": {"social_media": [], "websites": []},
            "metadata": {
                "sources_used": list(sources.keys()),
                "data_quality": "low",
                "consolidation_method": "basic"
            }
        }
        
        # Simple aggregation - just collect all data
        for source_name, source_data in sources.items():
            if isinstance(source_data, dict) and 'results' in source_data:
                for result in source_data.get('results', []):
                    if isinstance(result, dict):
                        # Extract phones
                        if 'phones' in result:
                            consolidated['contact']['phones'].extend(result['phones'])
                        
                        # Extract emails
                        if 'emails' in result:
                            consolidated['contact']['emails'].extend(result['emails'])
                        
                        # Extract addresses
                        if 'addresses' in result:
                            consolidated['contact']['addresses'].extend(result['addresses'])
        
        return consolidated
