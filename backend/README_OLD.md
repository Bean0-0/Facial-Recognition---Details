# I-XRAY Backend

Python backend for the I-XRAY people information aggregation system using **web scraping** and **open-source tools**.

## Features

- **Web Scraping**: No API keys required for most features!
- **People Aggregators**: Scrapes FastPeopleSearch, CheckThem, and Instant Checkmate
- **Search Engines**: Scrapes Google and Bing search results with advanced operators
- **Social Media**: Searches across Facebook, Twitter, Instagram, LinkedIn, GitHub, Reddit
- **LLM Integration** (Optional): Uses OpenAI/Anthropic for advanced data correlation
- **Async API**: FastAPI with full async support for concurrent searches

## Quick Start

```bash
cd backend
./start.sh
```

That's it! The server will be running at `http://localhost:8000`

## Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (API keys are optional)
cp .env.example .env

# Start server
python main.py
```

## Configuration (All Optional!)

The system works WITHOUT any API keys using web scraping. However, you can optionally add:

**LLM (for better data correlation):**
- OpenAI GPT-4 or Anthropic Claude for intelligent name extraction
- Without LLM: Uses regex-based extraction (still functional)

**Search Engine APIs (optional):**
- Google Custom Search / Bing API for official APIs
- Without: Uses web scraping (default, works fine)

Edit `.env` to add keys (all optional):
```bash
# Optional: Better data correlation
OPENAI_API_KEY=your_key_here

# Optional: If you want official search APIs
GOOGLE_API_KEY=your_key_here
GOOGLE_CSE_ID=your_id_here
```

## API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## API Endpoints

### Main Search
```http
POST /api/search
```

Search for a person using any combination of:
```json
{
  "name": "John Smith",
  "location": "Portland, OR",
  "email": "john@example.com",
  "phone": "555-1234",
  "username": "jsmith"
}
```

**Response includes:**
- Public records (addresses, phone numbers, relatives)
- Social media profiles
- Search engine results
- LLM-consolidated profile (if configured)

### Other Endpoints
- `GET /api/sources` - List all data sources
- `POST /api/search/source/{name}` - Search specific source
- `POST /api/llm/extract-names` - Extract names from text
- `POST /api/llm/correlate` - Correlate data from multiple sources

## Data Sources

### People Aggregators (Web Scraping)
- **FastPeopleSearch**: Public records, addresses, phones, relatives
- **CheckThem**: Background checks and people search
- **Instant Checkmate**: Comprehensive background reports

### Search Engines (Web Scraping)
- **Google**: Advanced operators for precise searches
  - `site:`, `filetype:`, `intext:`, `OR`, `AND`, `-`
- **Bing**: Alternative search with unique operators
  - `LinkFromDomain:`, `Contains:`

### Social Media (Direct Checks + Scraping)
- Facebook, Twitter, Instagram, LinkedIn
- GitHub (API), Reddit (API)
- TikTok, YouTube

### Reverse Image Search
- **Note**: PimEyes and FaceCheck.ID require paid subscriptions
- **Free alternatives**: 
  - Google Images Reverse Search
  - TinEye
  - Yandex Images

## How It Works

1. **Multi-Source Aggregation**: Queries multiple sources in parallel
2. **Advanced Search Operators**: Uses Google/Bing dorking techniques
3. **Web Scraping**: Parses HTML results from public websites
4. **Data Correlation**: Combines results from all sources
5. **LLM Processing** (optional): Intelligently links data and resolves conflicts

## Architecture

```
backend/
├── main.py                 # FastAPI application
├── services/
│   ├── aggregator.py       # Coordinates all searches
│   ├── llm_processor.py    # Optional LLM integration
│   └── sources/            # Individual scrapers
│       ├── fast_people_search.py
│       ├── check_them.py
│       ├── instant_checkmate.py
│       ├── search_engine.py
│       └── social_media.py
├── requirements.txt
└── .env.example
```

## Privacy & Legal Notice

This tool aggregates **publicly available information** from the internet.

**Legitimate Use Cases:**
- Verify your own online presence
- Security research
- OSINT training
- Background checks (where legally permitted)

**Important:**
- ✅ Always obtain proper consent
- ✅ Respect privacy laws (GDPR, CCPA, etc.)
- ✅ Use ethically and responsibly
- ⚠️ Some websites have Terms of Service restrictions
- ⚠️ Web scraping may be rate-limited

## Example Usage

```bash
# Search by name and location
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"name": "John Smith", "location": "Portland, OR"}'

# Search by email
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}'

# Search by username across social media
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"username": "jsmith"}'
```

## Development

```bash
# Run with auto-reload
uvicorn main:app --reload

# Run tests
pytest

# Format code
black .
```

## Troubleshooting

**"No module named 'fastapi'"**
- Make sure virtual environment is activated: `source venv/bin/activate`

**"No LLM configured" warning**
- This is normal! The system works without LLM using regex extraction
- Add OpenAI/Anthropic key to `.env` for better results

**Rate limiting / blocked by websites**
- Web scraping may trigger rate limits
- Use delays between requests
- Consider rotating user agents

## License

MIT License - See LICENSE file for details

**Disclaimer**: This tool is for educational and legitimate purposes only. Users are responsible for complying with applicable laws and website Terms of Service.
