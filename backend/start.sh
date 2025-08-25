#!/bin/bash
set -e

echo "🚀 Starting Smart Summary Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./build.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env file with your GEMINI_API_KEY"
    exit 1
fi

# Check if GEMINI_API_KEY is set
if ! grep -q "GEMINI_API_KEY=.*[^[:space:]]" .env; then
    echo "⚠️  Warning: GEMINI_API_KEY not found in .env file!"
    echo "Please add your Gemini API key to .env file"
    exit 1
fi

echo "✅ Environment configured"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/api/v1/health"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000