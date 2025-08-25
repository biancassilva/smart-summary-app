# Smart Summary App - Backend API

A high-performance FastAPI backend application with Google Gemini AI integration, designed for intelligent text summarization with real-time streaming capabilities.

## Features

- 🚀 **FastAPI Framework** - High-performance async Python web framework
- 🤖 **Google Gemini Integration** - Advanced AI text summarization using Gemini 1.5 Flash
- 📡 **Real-time Streaming** - Server-Sent Events (SSE) for live response delivery
- 🏗️ **Modular Architecture** - Clean, maintainable, and extensible codebase
- 🔧 **Robust Error Handling** - Comprehensive exception management and logging
- 📋 **Type Safety** - Full Pydantic validation for requests and responses
- 🌐 **CORS Ready** - Configured for seamless frontend integration
- 📊 **Health Monitoring** - Built-in health check and readiness endpoints
- 🔒 **Secure Configuration** - Environment-based settings management
- ⚡ **Performance Optimized** - Streaming chunked responses for better UX

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── core/
│   │   ├── config.py        # Environment configuration and settings
│   │   └── exceptions.py    # Custom exception handlers and middleware
│   ├── api/
│   │   ├── dependencies.py  # Dependency injection and common dependencies
│   │   └── v1/
│   │       ├── router.py    # Main API router v1
│   │       └── endpoints/
│   │           ├── chat.py  # Chat streaming endpoints
│   │           └── health.py # Health check endpoints
│   ├── services/
│   │   └── gemini_service.py # Google Gemini AI service integration
│   └── schemas/
│       ├── chat.py          # Chat request/response models
│       └── common.py        # Shared response schemas
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Environment configuration (not in git)
└── README.md              # This documentation
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone and setup environment:**

```bash
# Clone the repository
git clone <repository-url>
cd smart-summary-app/backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

2. **Environment configuration:**

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your configuration
nano .env  # or use your preferred editor
```

Required environment variables in `.env`:

```env
# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_OUTPUT_TOKENS=8192

# Application Settings
ENVIRONMENT=development
DEBUG=true

# CORS Settings (adjust for your frontend)
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3004"]
```

3. **Run the application:**

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the development server (recommended)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Alternative: Run directly
python app/main.py
```

4. **Verify installation:**

Visit http://localhost:8000/docs to see the interactive API documentation, or check the health endpoint:

```bash
curl http://localhost:8000/api/v1/health
```

## ⚡ Quick Reference

### Essential Commands

```bash
# Quick setup (recommended)
./build.sh && ./start.sh

# Manual setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Then edit with your GEMINI_API_KEY
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker setup
docker build -t smart-summary-backend .
docker run -p 8000:8000 --env-file .env smart-summary-backend

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Important URLs

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Main Endpoint**: POST http://localhost:8000/api/v1/chat/stream

### Key Files

- `app/main.py` - Application entry point
- `app/core/config.py` - Configuration settings
- `app/services/gemini_service.py` - AI service integration
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create from .env.example)
- `Dockerfile` - Container configuration
- `build.sh` - Development setup script
- `start.sh` - Development server script

## API Endpoints

### Health Checks

- `GET /` - Root endpoint
- `GET /api/v1/health` - Detailed health check
- `GET /api/v1/health/ready` - Readiness probe
- `GET /api/v1/health/live` - Liveness probe

### Chat Endpoints

- `POST /api/v1/chat/stream` - **Text summarization with streaming** (Primary endpoint)

### Example Usage

**Streaming Text Summarization:**

```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "# Understanding Machine Learning\n\nMachine learning is a subset of artificial intelligence (AI) that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. Machine learning focuses on the development of computer programs that can access data and use it learn for themselves...",
    "conversation_history": [],
    "temperature": 0.7
  }'
```

**Response Format:**

The API returns Server-Sent Events (SSE) with the following format:

```
data: {"content": "## Summary", "model": "gemini-1.5-flash", "is_complete": false}
data: {"content": "\n\nMachine learning is", "model": "gemini-1.5-flash", "is_complete": false}
data: {"content": " a powerful AI subset...", "model": "gemini-1.5-flash", "is_complete": false}
data: {"content": "", "model": "gemini-1.5-flash", "is_complete": true, "usage": {"prompt_tokens": 150, "completion_tokens": 85, "total_tokens": 235}}
data: [DONE]
```

## 🏗️ Architecture Explanations and Assumptions

### Core Architecture Principles

**1. Layered Architecture:**

```
Frontend (Next.js) ↔ API Layer ↔ Service Layer ↔ External AI (Gemini)
```

**2. Separation of Concerns:**

- **API Layer**: Request/response handling, validation, routing
- **Service Layer**: Business logic, AI integration, data processing
- **Schema Layer**: Type definitions, validation rules
- **Configuration Layer**: Environment management, settings

**3. Key Assumptions:**

- **Text-focused Processing**: Optimized for article, email, and document summarization
- **Streaming First**: All AI interactions use streaming for better UX
- **Stateless Design**: No session management, each request is independent
- **Markdown Output**: AI responses are formatted in markdown for rich display
- **Single Model**: Currently uses Gemini 1.5 Flash for optimal speed/quality balance

### Design Decisions

**Streaming Implementation:**

- Uses Server-Sent Events (SSE) for real-time response delivery
- Chunks responses for immediate user feedback
- Handles connection drops gracefully

**Error Management:**

- Structured error responses with proper HTTP status codes
- Graceful AI service failure handling
- Request validation before processing

**Performance Optimizations:**

- Async/await throughout the application
- Minimal memory footprint with streaming
- Efficient token usage tracking

## 🚀 Ideas for Future Improvements

### Feature Enhancements

**1. Multi-Model Support:**

```python
# Support for different AI models based on use case
models = {
    "fast": "gemini-1.5-flash",      # Quick summaries
    "detailed": "gemini-1.5-pro",   # Deep analysis
    "code": "code-bison",            # Code summarization
}
```

**2. Advanced Summarization Options:**

- Summary length control (short, medium, detailed)
- Multiple summary formats (bullet points, paragraphs, executive summary)
- Language detection and multi-language support
- Custom summary templates for different content types

**3. Content Processing:**

- File upload support (PDF, DOCX, TXT)
- URL content extraction and summarization
- Batch processing for multiple documents
- Content type detection and optimization

**4. User Experience:**

- Summary history and favorites
- Export options (PDF, DOCX, markdown)
- Summary comparison and merging
- Real-time collaboration features

**5. Integration Features:**

- Webhook notifications
- REST API for third-party integrations
- Browser extension support
- Slack/Teams bot integration

### Technical Improvements

**1. Caching Layer:**

```python
# Redis-based caching for frequent requests
@lru_cache(maxsize=1000)
async def cached_summary(content_hash: str) -> str:
    # Return cached summary if available
    pass
```

**2. Queue System:**

- Background job processing with Celery
- Priority queues for different request types
- Batch processing optimization

**3. Advanced Monitoring:**

- Request tracing and performance metrics
- AI model usage analytics
- Cost tracking and optimization
- Real-time health dashboards

## 🔒 Scaling and Security Considerations

### Scaling Strategies

**1. Horizontal Scaling:**

```bash
# Multiple application instances behind load balancer
# Each instance handles streaming independently
uvicorn app.main:app --port 8001 --workers 4
uvicorn app.main:app --port 8002 --workers 4
# + nginx load balancer
```

**2. Vertical Scaling:**

- Optimize for I/O-bound operations (AI API calls)
- Memory usage is minimal due to streaming
- CPU usage depends on request volume, not content size

**3. Database Considerations:**

```python
# Future database integration for user management
# Recommended: PostgreSQL with async drivers
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/smart_summary_app"
```

**4. Caching Strategy:**

- Redis for frequently requested summaries
- CDN for static content
- Application-level caching for configuration

### Security Implementations

**1. API Security:**

```python
# Rate limiting (recommended implementation)
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/v1/chat/stream")
@limiter.limit("10/minute")  # Prevent abuse
async def stream_chat(request: Request):
    pass
```

**2. Input Validation & Sanitization:**

- Pydantic models for request validation
- Content length limits (currently 50,000 chars)
- Input sanitization to prevent injection attacks

**3. Environment Security:**

```env
# Production security settings
ENVIRONMENT=production
DEBUG=false
GEMINI_API_KEY=your_secure_key_here
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

**4. Infrastructure Security:**

- HTTPS enforcement in production
- API key rotation strategy
- Request logging and monitoring
- CORS configuration for specific domains only

## 🚀 Building the Backend

### Development Build (Quick Start)

**Option 1: Using Build Scripts (Recommended)**

```bash
# Build and set up environment
./build.sh

# Start development server
./start.sh
```

**Option 2: Manual Setup**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Test the build
python -c "import app.main; print('✅ Backend ready')"

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment

**1. Container Deployment (Recommended):**

The backend includes a complete `Dockerfile` for production deployment:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run with Docker:**

```bash
# Build the image
docker build -t smart-summary-backend .

# Run with environment file
docker run -p 8000:8000 --env-file .env smart-summary-backend

# Or run with environment variables
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key_here \
  -e ENVIRONMENT=production \
  -e DEBUG=false \
  smart-summary-backend
```

**2. Direct Production Server:**

```bash
# Set production environment variables
export ENVIRONMENT=production
export DEBUG=false

# Run with multiple workers for production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**3. Process Management:**

```bash
# Using systemd for production
sudo systemctl enable smart-summary-backend
sudo systemctl start smart-summary-backend
```

### Build Scripts

The backend includes convenient build scripts:

**`build.sh`** - Sets up the development environment:

- Creates virtual environment
- Installs dependencies
- Sets up configuration files
- Tests the installation

**`start.sh`** - Starts the development server:

- Activates virtual environment
- Validates configuration
- Starts uvicorn with reload for development

### Build Troubleshooting

**Common Build Issues:**

1. **Permission denied for build scripts:**

   ```bash
   chmod +x build.sh start.sh
   ```

2. **Virtual environment not found:**

   ```bash
   # Run build script first
   ./build.sh
   ```

3. **Missing GEMINI_API_KEY:**

   ```bash
   # Check your .env file
   cat .env | grep GEMINI_API_KEY

   # Add your API key
   echo "GEMINI_API_KEY=your_key_here" >> .env
   ```

4. **Port 8000 already in use:**

   ```bash
   # Kill existing process
   lsof -ti:8000 | xargs kill -9

   # Or use different port
   uvicorn app.main:app --port 8001
   ```

**Docker Build Issues:**

1. **Docker not installed:**

   ```bash
   # Install Docker Desktop or Docker Engine
   # Then verify installation
   docker --version
   ```

2. **Build fails during pip install:**

   ```bash
   # Clean build (no cache)
   docker build --no-cache -t smart-summary-backend .
   ```

3. **Container fails to start:**

   ```bash
   # Check logs
   docker logs <container_id>

   # Run interactively for debugging
   docker run -it smart-summary-backend /bin/bash
   ```

**3. Monitoring & Logging:**

- Structured logging with proper log levels
- Health check endpoints for monitoring
- Error tracking (e.g., Sentry integration)
- Performance metrics collection

**4. Backup & Recovery:**

- Configuration backup strategy
- API usage metrics preservation
- Disaster recovery procedures

## 🔧 Development & Testing

### Development Workflow

**1. Adding New Features:**

```bash
# 1. Create feature branch
git checkout -b feature/new-summarization-type

# 2. Add endpoint in app/api/v1/endpoints/
# 3. Define schemas in app/schemas/
# 4. Implement service logic in app/services/
# 5. Register routes in app/api/v1/router.py

# 6. Test locally
uvicorn app.main:app --reload

# 7. Test with frontend integration
```

**2. Testing Endpoints:**

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Interactive API docs
open http://localhost:8000/docs

# Test streaming with curl
curl -N -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test content for summarization"}'
```

**3. Code Quality:**

```bash
# Format code (if using black)
black app/

# Type checking (if using mypy)
mypy app/

# Lint code (if using flake8)
flake8 app/
```

### Frontend Integration Guide

**Next.js/React Integration:**

```typescript
// lib/api.ts - Complete streaming implementation
export async function streamSummarization({
  message,
  onChunk,
  onComplete,
  onError,
}: {
  message: string;
  onChunk?: (chunk: { content: string; model: string }) => void;
  onComplete?: () => void;
  onError?: (error: Error) => void;
}) {
  try {
    const response = await fetch("/api/v1/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, conversation_history: [] }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) throw new Error("No response body");

    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6).trim();
          if (data === "[DONE]") {
            onComplete?.();
            return;
          }

          try {
            const parsed = JSON.parse(data);
            if (parsed.content || parsed.is_complete) {
              onChunk?.(parsed);
            }
          } catch (parseError) {
            console.warn("Failed to parse chunk:", data);
          }
        }
      }
    }
  } catch (error) {
    onError?.(error instanceof Error ? error : new Error("Unknown error"));
  }
}
```

---

## 📞 Support & Contributing

### Getting Help

- **Documentation**: Check this README and API docs at `/docs`
- **Issues**: Report bugs and request features in the project repository
- **Health Check**: Always verify with `/api/v1/health` if something isn't working

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🌐 Deployment

### Render Deployment

The backend includes a `render.yaml` configuration for easy deployment on Render:

**1. Environment Variables Setup:**

Set these environment variables in your Render service:

```bash
# Required (Set as Secret)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (good defaults)
ENVIRONMENT=production
DEBUG=false
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=100000
STREAMING_CHUNK_SIZE=2
STREAMING_DELAY_MS=50
LOG_LEVEL=INFO
```

**2. Deploy Command:**

Render will automatically use:

```bash
# Build command
pip install -r requirements.txt

# Start command
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**3. Troubleshooting Render Deployment:**

- **Configuration Error**: The backend now ignores unknown environment variables, so old configs won't cause errors
- **Missing GEMINI_API_KEY**: Set this as a secret environment variable in Render dashboard
- **Port Issues**: Render automatically sets `$PORT` - no configuration needed
- **Build Failures**: Check that `requirements.txt` is in the root of your service directory

### Other Deployment Platforms

**Vercel (Serverless):**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Railway:**

```bash
# Connect your repo and Railway will auto-deploy
# Set GEMINI_API_KEY in environment variables
```

**Heroku:**

```bash
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create smart-summary-backend
heroku config:set GEMINI_API_KEY=your_key_here
git push heroku main
```

---

**Built with ❤️ using FastAPI and Google Gemini AI**
