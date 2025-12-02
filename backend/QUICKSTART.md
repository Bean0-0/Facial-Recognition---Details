## Quick Start with FREE Google Gemini

The backend now supports **Google Gemini 1.5 Flash** which is completely FREE!

### 1. Get Your Free Gemini API Key

Visit: https://makersuite.google.com/app/apikey

1. Sign in with your Google account
2. Click "Create API Key"
3. Copy the API key

### 2. Configure the Backend

Edit `/backend/.env` and add your Gemini API key:

```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Install & Run

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

That's it! The system will:
- ✅ Use FREE Gemini for name extraction and data correlation
- ✅ Work without any paid APIs
- ✅ Scrape all sources directly (no API keys needed for most features)

### Optional APIs

All other API keys are optional:
- Face search APIs (PimEyes, FaceCheck) - uses scraping as fallback
- Search APIs (Google, Bing) - uses scraping as fallback
- Other LLMs (OpenAI, Anthropic) - Gemini is free and works great!

### API Endpoints

Once running on `http://localhost:8000`:
- 📖 Docs: http://localhost:8000/docs
- 🔍 Search: `POST /api/search`
- 💊 Health: `GET /health`

### Example Search

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "location": "Portland, OR"
  }'
```
