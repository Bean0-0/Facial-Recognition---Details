# I-XRAY Backend 🔍

Python backend for the I-XRAY people information aggregation system.

## ⚡ Quick Start (100% FREE!)

**No paid APIs required!** Get started in 3 minutes:

1. **Get a FREE Gemini API key**: https://makersuite.google.com/app/apikey
2. **Configure**: Edit `.env` and add `GEMINI_API_KEY=your_key_here`
3. **Run**: `./start.sh` or manually:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## ✨ Features

- ✅ **FREE LLM**: Google Gemini 1.5 Flash (completely free!)
- ✅ **No API Dependencies**: Works with pure web scraping
- ✅ **Reverse Face Search**: PimEyes and FaceCheck.ID integration
- ✅ **People Aggregators**: FastPeopleSearch, CheckThem, Instant Checkmate
- ✅ **Search Engines**: Google/Bing with advanced operators
- ✅ **Social Media**: Facebook, Twitter, Instagram, LinkedIn, GitHub, Reddit
- ✅ **LLM Correlation**: Automatic name extraction and data consolidation
- ✅ **Async API**: FastAPI with concurrent searches for speed

## 🚀 Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure (add your FREE Gemini API key)
cp .env.example .env
nano .env  # Edit and add GEMINI_API_KEY
```

## ⚙️ Configuration

Edit `.env`:

```bash
# FREE Google Gemini (RECOMMENDED)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_free_gemini_key_here

# All other APIs are OPTIONAL
# System works with web scraping if not provided
PIMEYES_API_KEY=
FACECHECK_API_KEY=
GOOGLE_API_KEY=
BING_API_KEY=
```

### Get Your FREE Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy and paste into `.env`

## 🎯 Running the Server

```bash
# Method 1: Use start script
./start.sh

# Method 2: Run directly
python main.py

# Method 3: Use uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔌 API Endpoints

### Main Search
```http
POST /api/search
Content-Type: application/json

{
  "name": "John Smith",
  "location": "Portland, OR",
  "email": "john@example.com",
  "phone": "555-1234",
  "username": "jsmith",
  "image": "base64_or_url"
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "location": "Portland, OR"
  }'
```

### Response Format
```json
{
  "search_id": "uuid",
  "timestamp": "2025-12-02T...",
  "query": {...},
  "sources": {
    "pimeyes": {...},
    "facecheck": {...},
    "fastpeoplesearch": {...},
    "checkthem": {...},
    "instantcheckmate": {...},
    "searchengine": {...},
    "socialmedia": {...}
  },
  "consolidated": {
    "person": {
      "name": "John Smith",
      "age": "35-40",
      "confidence": 0.95
    },
    "contact": {
      "phones": [...],
      "emails": [...],
      "addresses": [...]
    },
    "relationships": {
      "relatives": [...],
      "associates": [...]
    },
    "online_presence": {
      "social_media": [...],
      "websites": [...]
    }
  }
}
```

### Other Endpoints

```http
GET  /api/sources              # List all available data sources
POST /api/search/source/{name}  # Search specific source
POST /api/llm/extract-names     # Extract names from text
POST /api/llm/correlate         # Correlate data from sources
GET  /health                    # Health check
```

## 🗂️ Data Sources

### Reverse Face Search
- **PimEyes**: Reverse image search across the web (scraping/API)
- **FaceCheck.ID**: Face recognition search engine (scraping/API)

### People Aggregators  
- **FastPeopleSearch**: Public records, addresses, phone numbers, relatives
- **CheckThem**: Background checks and people search
- **Instant Checkmate**: Comprehensive background reports

### Search Engines
- **Google**: Advanced operators for precise searches (scraping)
- **Bing**: Alternative search with unique operators (scraping)

### Social Media
- Facebook, Twitter, Instagram, LinkedIn
- GitHub, Reddit, TikTok, YouTube

## 🏗️ Architecture

```
backend/
├── main.py                      # FastAPI application
├── services/
│   ├── aggregator.py            # Main coordinator
│   ├── llm_processor.py         # Gemini/OpenAI/Anthropic
│   └── sources/                 # Data source scrapers
│       ├── pimeyes.py
│       ├── facecheck.py
│       ├── fast_people_search.py
│       ├── check_them.py
│       ├── instant_checkmate.py
│       ├── search_engine.py
│       └── social_media.py
├── requirements.txt
├── .env.example
└── README.md
```

## 🔒 Privacy & Legal Notice

This tool is designed for **educational purposes** and legitimate use cases:
- ✅ Verifying your own online presence
- ✅ Security research
- ✅ OSINT training
- ✅ Cybersecurity education

**Important:**
- ⚠️ Always obtain proper consent before searching for others
- ⚠️ Respect privacy and applicable laws (GDPR, CCPA, etc.)
- ⚠️ Use responsibly and ethically
- ⚠️ Some sources may have Terms of Service restrictions

## 🛠️ Development

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
pytest

# Format code
black .

# Type checking
mypy .
```

## 💡 Tips

1. **Start with Gemini**: It's free and works great for most use cases
2. **No APIs Needed**: Most features work with web scraping alone
3. **Rate Limiting**: Add delays between requests to avoid being blocked
4. **VPN/Proxy**: Consider using a VPN for privacy when scraping
5. **Respect Robots.txt**: The scrapers should respect robots.txt files

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

- **Documentation**: http://localhost:8000/docs
- **Issues**: Create a GitHub issue
- **Gemini API**: https://ai.google.dev/docs

---

**Made with ❤️ for ethical OSINT research**
