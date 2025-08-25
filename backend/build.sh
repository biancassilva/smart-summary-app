#!/bin/bash
set -e

echo "🚀 Building Smart Summary Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check environment file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📋 Copying .env.example to .env..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✏️  Please edit .env and add your GEMINI_API_KEY"
    else
        echo "❌ .env.example not found. Please create .env file manually."
    fi
fi

# Test import
echo "🧪 Testing backend imports..."
python -c "import app.main; print('✅ Backend imports successfully')"

echo "✅ Build completed successfully!"
echo ""
echo "🚀 To start the backend:"
echo "   ./start.sh"
echo ""
echo "📚 API Documentation will be available at:"
echo "   http://localhost:8000/docs"
echo ""
echo "💡 Don't forget to configure your GEMINI_API_KEY in .env"