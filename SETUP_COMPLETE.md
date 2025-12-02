# I-XRAY Backend - Setup Complete! ✅

## What's Been Built

A **complete Python backend** for aggregating people information from multiple sources, now using **100% FREE Google Gemini** for AI-powered data correlation!

## 🎯 Key Changes Made

### 1. **FREE Google Gemini Integration**
- ✅ Added support for Google Gemini 1.5 Flash (completely free!)
- ✅ Set as default LLM provider
- ✅ Fallback support for OpenAI and Anthropic (optional)
- ✅ Works without any LLM if none configured (regex fallback)

### 2. **No API Dependencies**
- ✅ All data sources work with web scraping
- ✅ APIs are completely optional
- ✅ Face search, people search, social media all scrape-based
- ✅ Google/Bing searches use web scraping by default

### 3. **Complete Backend Structure**

```
backend/
├── main.py                          # FastAPI app with async endpoints
├── services/
│   ├── aggregator.py                # Coordinates all sources
│   ├── llm_processor.py             # Gemini/OpenAI/Anthropic support
│   └── sources/
│       ├── pimeyes.py               # Reverse face search
│       ├── facecheck.py             # Face recognition
│       ├── fast_people_search.py    # Public records scraper
│       ├── check_them.py            # Background checks
│       ├── instant_checkmate.py     # Comprehensive reports
│       ├── search_engine.py         # Google/Bing with operators
│       └── social_media.py          # Social platform searches
├── requirements.txt                 # Python dependencies
├── .env                            # Configuration (Gemini key here)
├── .env.example                    # Template
├── README.md                       # Full documentation
├── QUICKSTART.md                   # Quick start guide
└── start.sh                        # Easy start script
```

## 🚀 How to Start

### Option 1: Quick Start (Recommended)
```bash
cd backend
./start.sh
```

### Option 2: Manual Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your FREE Gemini API key to .env
# Get key at: https://makersuite.google.com/app/apikey
nano .env  # Add: GEMINI_API_KEY=your_key_here

# Start server
python main.py
```

Server runs at: **http://localhost:8000**
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## 📡 API Usage Example

```bash
# Search for a person
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "location": "Portland, OR",
    "email": "john@example.com"
  }'
```

## 🔑 Getting Your FREE Gemini API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Add to `.env`: `GEMINI_API_KEY=your_key_here`

That's it! No credit card, no payment, completely free!

## 🎯 What Each Source Does

### Phase 1: Reverse Face Search (if image provided)
- **PimEyes**: Searches web for matching faces
- **FaceCheck**: Face recognition across social media
- **LLM**: Extracts names from found matches

### Phase 2: People Aggregators (if name/contact info provided)
- **FastPeopleSearch**: Public records, addresses, phones, relatives
- **CheckThem**: Background checks, criminal records
- **Instant Checkmate**: Comprehensive background reports

### Phase 3: Search Engines (if name/email/username provided)
- **Google**: Advanced operators (site:, filetype:, etc.)
- **Bing**: Alternative search with unique operators
- Searches across LinkedIn, Facebook, documents, etc.

### Phase 4: Social Media (if name/username provided)
- Direct profile checks on: Twitter, Instagram, GitHub, Reddit
- Google dorking for: Facebook, LinkedIn, TikTok, YouTube

### Phase 5: LLM Consolidation
- **Gemini AI**: Consolidates all data
- Resolves conflicts between sources
- Infers relationships
- Assigns confidence scores
- Creates unified person profile

## 🔒 Privacy & Ethics

**This tool is for educational and legitimate purposes only:**
- ✅ Check your own online footprint
- ✅ Security research
- ✅ OSINT training
- ❌ Don't search others without consent
- ❌ Respect privacy laws (GDPR, CCPA)
- ❌ Don't violate Terms of Service

## 📊 Data Returned

The API returns comprehensive data:
- **Person**: Name, age, location (with confidence scores)
- **Contact**: Phones, emails, addresses (current/previous)
- **Relationships**: Relatives, associates
- **Online Presence**: Social media profiles, websites
- **Background**: Criminal records, court records, businesses
- **Metadata**: Sources used, data quality, timestamps

## 🛠️ Configuration Options

Edit `.env` to customize:

```bash
# LLM Provider (gemini is FREE and recommended)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key

# Optional: Other LLM providers
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Optional: API keys (works with scraping if not provided)
PIMEYES_API_KEY=
FACECHECK_API_KEY=
GOOGLE_API_KEY=
BING_API_KEY=

# Server settings
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 🎓 Learning Resources

- **Gemini API Docs**: https://ai.google.dev/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **OSINT Framework**: https://osintframework.com/
- **Google Dorking**: https://www.exploit-db.com/google-hacking-database

## ✨ Next Steps

1. **Get Gemini API key** (free, no credit card)
2. **Start the server** (`./start.sh`)
3. **Test the API** (visit http://localhost:8000/docs)
4. **Try a search** (use the example above)
5. **Integrate with frontend** (already built in `/public`)

## 🐛 Troubleshooting

**Server won't start?**
- Check Python version: `python3 --version` (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check .env file exists and has Gemini key

**No results from sources?**
- Some sites may block scrapers (use VPN/proxy)
- Rate limiting may apply (add delays)
- Check logs for specific errors

**LLM not working?**
- Verify Gemini API key is correct
- Check internet connection
- System will fallback to regex if LLM fails

---

**You're all set! 🎉**

The backend is fully functional with FREE Google Gemini integration. No paid APIs required!
