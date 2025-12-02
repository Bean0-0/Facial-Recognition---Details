#!/bin/bash
# Complete setup and start script

echo "🚀 I-XRAY Backend - Complete Setup"
echo "===================================="
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Check Python
echo "📍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing dependencies (this may take a minute)..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Check if .env exists and has Gemini key
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
fi

# Check for Gemini API key
if ! grep -q "^GEMINI_API_KEY=.\\+" .env; then
    echo "⚠️  GEMINI_API_KEY not found in .env"
    echo ""
    echo "📝 To get started, you need a FREE Gemini API key:"
    echo "   1. Visit: https://makersuite.google.com/app/apikey"
    echo "   2. Sign in with your Google account"
    echo "   3. Click 'Create API Key'"
    echo "   4. Copy the key"
    echo "   5. Edit .env and set: GEMINI_API_KEY=your_key_here"
    echo ""
    read -p "Press Enter to continue anyway (system will work with limited features)..."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📖 API Documentation: http://localhost:8000/docs"
echo "💚 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "===================================="
echo ""

# Start the server
python main.py
