"""
I-XRAY Backend - People Information Aggregator
Main FastAPI application with async support
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
from datetime import datetime

from services.aggregator import PeopleDataAggregator
from services.llm_processor import LLMProcessor

app = FastAPI(
    title="I-XRAY API",
    description="Automated people information aggregation system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
aggregator = PeopleDataAggregator()
llm_processor = LLMProcessor()


class SearchRequest(BaseModel):
    """Search request model"""
    name: Optional[str] = Field(None, description="Person's full name")
    image: Optional[str] = Field(None, description="Base64 encoded image or image URL")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    username: Optional[str] = Field(None, description="Social media username")
    address: Optional[str] = Field(None, description="Physical address")
    location: Optional[str] = Field(None, description="City, State or general location")


class SearchResponse(BaseModel):
    """Search response model"""
    search_id: str
    timestamp: str
    query: Dict[str, Any]
    sources: Dict[str, Any]
    consolidated: Optional[Dict[str, Any]]
    status: str


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "I-XRAY API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "search": "/api/search",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "aggregator": "operational",
            "llm": "operational" if llm_processor.is_configured() else "not_configured"
        }
    }


@app.post("/api/search", response_model=SearchResponse)
async def search_person(request: SearchRequest, background_tasks: BackgroundTasks):
    """
    Main search endpoint - aggregates data from multiple sources
    
    This endpoint performs comprehensive person searches across:
    - Reverse face search (PimEyes, FaceCheck.ID)
    - People search aggregators (FastPeopleSearch, CheckThem, Instant Checkmate)
    - Search engines (Google, Bing with advanced operators)
    - Social media platforms (Facebook, Twitter, Instagram, LinkedIn, etc.)
    
    Results are correlated using LLM to identify relationships and consolidate data.
    """
    try:
        # Validate at least one search parameter is provided
        if not any([request.name, request.image, request.email, 
                   request.phone, request.username, request.address]):
            raise HTTPException(
                status_code=400,
                detail="At least one search parameter must be provided"
            )
        
        # Convert request to dict
        query = request.dict(exclude_none=True)
        
        # Perform aggregation
        results = await aggregator.aggregate_person_data(query)
        
        return SearchResponse(
            search_id=results["search_id"],
            timestamp=results["timestamp"],
            query=query,
            sources=results["sources"],
            consolidated=results.get("consolidated"),
            status="completed"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sources")
async def get_available_sources():
    """Get list of available data sources"""
    return {
        "sources": aggregator.get_available_sources(),
        "categories": {
            "reverse_face_search": ["pimeyes", "facecheck"],
            "people_aggregators": ["fastpeoplesearch", "checkthem", "instantcheckmate"],
            "search_engines": ["google", "bing"],
            "social_media": ["facebook", "twitter", "instagram", "linkedin", "github", "reddit"]
        }
    }


@app.post("/api/search/source/{source_name}")
async def search_specific_source(source_name: str, request: SearchRequest):
    """Search a specific data source"""
    try:
        query = request.dict(exclude_none=True)
        results = await aggregator.search_source(source_name, query)
        
        return {
            "source": source_name,
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "results": results
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/llm/extract-names")
async def extract_names_from_text(text: str):
    """Extract person names from text using LLM"""
    try:
        names = await llm_processor.extract_names(text)
        return {
            "text": text,
            "extracted_names": names,
            "count": len(names)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/llm/correlate")
async def correlate_data(data: Dict[str, Any]):
    """Use LLM to correlate and consolidate data from multiple sources"""
    try:
        consolidated = await llm_processor.consolidate_person_data(data)
        return {
            "consolidated": consolidated,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
