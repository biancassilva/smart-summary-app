# FastAPI Backend with OpenAI Integration

A scalable FastAPI backend application with OpenAI integration and server-side streaming capabilities.

## Features

- 🚀 FastAPI with async/await support
- 🤖 OpenAI GPT integration with streaming
- 📡 Server-Sent Events (SSE) for real-time responses
- 🏗️ Modular, scalable architecture
- 🔧 Comprehensive error handling
- 📋 Request/response validation with Pydantic
- 🌐 CORS support for frontend integration
- 📊 Health check endpoints
- 🔒 Environment-based configuration

## Project Structure

```
fastapi-backend/
├── app/
│   ├── main.py              # Application entry point
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   └── exceptions.py    # Custom exception handlers
│   ├── api/
│   │   ├── dependencies.py  # Dependency injection
│   │   └── v1/
│   │       ├── router.py    # API router
│   │       └── endpoints/   # API endpoints
│   ├── services/
│   │   └── openai_service.py # OpenAI integration
│   └── schemas/
│       ├── chat.py          # Chat-related models
│       └── common.py        # Common response models
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. **Clone and setup environment:**

```bash
git clone <repository>
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. **Environment configuration:**

```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

3. **Run the application:**

```bash
# Activate virtual environment first
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run with uvicorn (recommended)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly (alternative)
python app/main.py
```

## API Endpoints

### Health Checks

- `GET /` - Root endpoint
- `GET /api/v1/health` - Detailed health check
- `GET /api/v1/health/ready` - Readiness probe
- `GET /api/v1/health/live` - Liveness probe

### Chat Endpoints

- `POST /api/v1/chat/completions` - Standard chat completion
- `POST /api/v1/chat/stream` - Streaming chat completion

### Example Usage

**Standard Chat:**

```bash
curl -X POST "http://localhost:8000/api/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "conversation_history": [],
    "stream": false
  }'
```

**Streaming Chat:**

```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me a story",
    "conversation_history": [],
    "temperature": 0.8
  }'
```

## Configuration

Key environment variables in `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
ENVIRONMENT=development
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3003"]
```

## Architecture Highlights

### Scalability Features:

- **Modular structure** - Easy to add new features
- **Dependency injection** - Clean service management
- **Async/await** - High concurrency support
- **Pydantic models** - Type safety and validation
- **Exception handling** - Robust error management
- **Configuration management** - Environment-based settings

### Streaming Implementation:

- Server-Sent Events (SSE) format
- Real-time response delivery
- Proper error handling in streams
- Client-friendly chunk formatting

## Development

**Add new endpoints:**

1. Create endpoint file in `app/api/v1/endpoints/`
2. Define Pydantic models in `app/schemas/`
3. Add business logic in `app/services/`
4. Register router in `app/api/v1/router.py`

**Testing:**

- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Production Deployment

1. Set `ENVIRONMENT=production` in `.env`
2. Configure proper `ALLOWED_ORIGINS`
3. Set up reverse proxy (nginx/Apache)
4. Use process manager (systemd/supervisor)
5. Configure logging and monitoring

## Frontend Integration

The API is designed to work seamlessly with modern frontend frameworks:

**JavaScript/TypeScript Example:**

```javascript
// Streaming chat
const response = await fetch("/api/v1/chat/stream", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    message: "Hello!",
    conversation_history: [],
  }),
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { value, done } = await reader.read();
  if (done) break;

  const chunk = decoder.decode(value);
  const lines = chunk.split("\n");

  for (const line of lines) {
    if (line.startsWith("data: ")) {
      const data = line.slice(6);
      if (data === "[DONE]") return;

      try {
        const parsed = JSON.parse(data);
        if (parsed.content) {
          console.log(parsed.content); // Handle streaming content
        }
      } catch (e) {
        // Handle parsing errors
      }
    }
  }
}
```
