# EasyMate Backend API Documentation

## Overview

The EasyMate backend is a sophisticated, scalable FastAPI application designed for intelligent text summarization using Google Gemini AI integration. The system specializes in processing and summarizing various types of content including articles, meeting notes, emails, and documents with structured markdown output.

## Table of Contents

- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Core Features](#core-features)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Deployment](#deployment)
- [Advantages & Benefits](#advantages--benefits)

## Architecture

The application follows a clean, layered architecture pattern:

```
┌─────────────────────────────────────────────────┐
│                  Client Layer                   │
│          (Frontend Applications)               │
└─────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│                API Gateway Layer                │
│        (FastAPI with CORS & Middleware)        │
└─────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│                Business Logic                   │
│            (Services & Endpoints)              │
└─────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│               External Services                 │
│              (Google Gemini AI)                │
└─────────────────────────────────────────────────┘
```

### Key Architectural Principles:

- **Separation of Concerns**: Clear separation between API routes, business logic, and external service integration
- **Dependency Injection**: Leverages FastAPI's dependency injection for service management
- **Asynchronous Processing**: Built with async/await patterns for optimal performance
- **Modular Design**: Organized into distinct modules for maintainability and scalability

## Technology Stack

### Core Framework & Libraries

| Technology | Version | Purpose | Advantages |
|------------|---------|---------|------------|
| **FastAPI** | >=0.104.0 | Web framework | High performance, automatic OpenAPI docs, type validation |
| **Uvicorn** | >=0.24.0 | ASGI server | Fast, production-ready async server |
| **Pydantic** | >=2.0.0 | Data validation | Type safety, automatic validation, serialization |
| **Google Generative AI** | >=0.3.0 | AI integration | Direct access to Gemini models |

### Supporting Libraries

- **python-dotenv**: Environment variable management
- **httpx**: Modern async HTTP client
- **python-multipart**: File upload support
- **pydantic-settings**: Configuration management

### Runtime Environment

- **Python**: 3.11+ (slim Docker image)
- **Container**: Docker with multi-stage builds
- **Deployment**: Cloud-ready with health checks

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py          # Dependency injection
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── chat.py         # Chat completions & streaming
│   │       │   └── health.py       # Health check endpoints
│   │       └── router.py           # API v1 router configuration
│   ├── core/
│   │   ├── config.py              # Application configuration
│   │   └── exceptions.py          # Custom exception handling
│   ├── schemas/
│   │   ├── chat.py               # Chat-related data models
│   │   └── common.py             # Shared data models
│   ├── services/
│   │   └── gemini_service.py     # Google Gemini AI integration
│   └── main.py                   # Application entry point
├── Dockerfile                    # Container configuration
├── requirements.txt             # Python dependencies
├── render.yaml                  # Render deployment config
├── build.sh                     # Build script
└── start.sh                     # Startup script
```

## Core Features

### 1. AI-Powered Text Summarization

- **Intelligent Processing**: Leverages Google Gemini 1.5 Flash for high-quality summarization
- **Markdown Formatting**: Automatically structures output with proper headings, lists, and emphasis
- **Content Type Adaptation**: Tailors summaries based on content type (articles, meetings, emails)
- **Conversation History**: Maintains context across multiple interactions

### 2. Streaming Response System

- **Real-time Streaming**: Server-Sent Events (SSE) for live response delivery
- **Word-by-Word Effect**: Configurable chunking for human-like typing simulation
- **Optimized Performance**: Async generators with minimal latency
- **Error Handling**: Robust error recovery during streaming

### 3. Production-Ready Architecture

- **Health Monitoring**: Multiple health check endpoints for deployment platforms
- **CORS Configuration**: Dynamic CORS handling for multiple environments
- **Security Middleware**: Trusted host validation for production environments
- **Comprehensive Logging**: Structured logging with configurable levels

## API Endpoints

### Root Endpoints

#### `GET /`
**Purpose**: Application information and navigation
**Response**:
```json
{
  "message": "Welcome to Smart Summary App - Backend API",
  "version": "1.0.0",
  "environment": "development",
  "docs": "/docs",
  "health": "/api/v1/health"
}
```

#### `GET /cors-debug`
**Purpose**: CORS configuration debugging
**Response**:
```json
{
  "allowed_origins": ["http://localhost:3000"],
  "environment": "development",
  "raw_allowed_origins": "http://localhost:3000"
}
```

### Health Check Endpoints

#### `GET /api/v1/health`
**Purpose**: Primary health check for monitoring systems
**Response Model**: `HealthResponse`
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "message": "Service is running properly"
}
```

#### `GET /api/v1/health/ready`
**Purpose**: Kubernetes/Docker readiness probe
**Response**: `{"status": "ready"}`

#### `GET /api/v1/health/live`
**Purpose**: Kubernetes/Docker liveness probe  
**Response**: `{"status": "alive"}`

### Chat Endpoints

#### `POST /api/v1/chat/completions`
**Purpose**: Non-streaming chat completions
**Request Model**: `ChatRequest`
```json
{
  "message": "Summarize this article about AI...",
  "conversation_history": [],
  "model": "gemini-1.5-flash",
  "temperature": 0.7,
  "max_tokens": 4000,
  "stream": false
}
```

**Response Model**: `ChatResponse`
```json
{
  "response": "# Article Summary\n\n## Key Points\n\n- Point 1\n- Point 2",
  "model": "gemini-1.5-flash",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 200,
    "total_tokens": 350
  },
  "message": "Chat completion successful"
}
```

#### `POST /api/v1/chat/stream`
**Purpose**: Streaming chat completions with SSE
**Request Model**: `ChatRequest`
**Response**: Server-Sent Events stream
```
id: 1
event: message
data: {"content": "# Article", "is_complete": false, "model": "gemini-1.5-flash"}

id: 2  
event: message
data: {"content": " Summary", "is_complete": false, "model": "gemini-1.5-flash"}

id: 3
event: done
data: [DONE]
```

## Configuration

### Environment Variables

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `GEMINI_API_KEY` | - | Google Gemini API key | ✅ |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini model to use | ❌ |
| `GEMINI_MAX_TOKENS` | `100000` | Maximum response tokens | ❌ |
| `GEMINI_TEMPERATURE` | `0.7` | Response creativity (0.0-2.0) | ❌ |
| `ENVIRONMENT` | `development` | Deployment environment | ❌ |
| `LOG_LEVEL` | `INFO` | Logging level | ❌ |
| `ALLOWED_ORIGINS` | Local URLs | CORS allowed origins | ❌ |
| `STREAMING_CHUNK_SIZE` | `2` | Words per streaming chunk | ❌ |
| `STREAMING_DELAY_MS` | `50` | Delay between chunks (ms) | ❌ |

### Configuration Management

The application uses Pydantic Settings for robust configuration management:

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
```

**Benefits:**
- **Type Safety**: Automatic type conversion and validation
- **Environment Integration**: Seamless .env file support
- **Error Prevention**: Fails fast on invalid configurations
- **Documentation**: Self-documenting configuration schema

## Error Handling

### Exception Hierarchy

```
Exception
├── GeminiServiceException     # AI service errors
├── CustomHTTPException        # Application-specific errors
└── HTTPException             # FastAPI standard errors
```

### Error Response Format

All errors follow a consistent JSON structure:

```json
{
  "error": {
    "message": "Detailed error description",
    "code": "ERROR_CODE",
    "status_code": 400
  }
}
```

### Error Types

1. **Gemini Service Errors**: AI API failures, quota exceeded, invalid requests
2. **Validation Errors**: Invalid input data, missing required fields
3. **Streaming Errors**: Connection issues, timeout errors
4. **General Errors**: Unexpected server errors with full logging

## Deployment

### Docker Configuration

The application uses a multi-stage Docker build for optimization:

```dockerfile
FROM python:3.11-slim
# Security: Non-root user
# Health checks: Built-in endpoint monitoring
# Optimization: Minimal dependencies, no cache
```

**Security Features:**
- Non-root user execution
- Minimal system dependencies  
- Environment variable injection
- Health check integration

### Deployment Platforms

**Render.com** (Primary):
```yaml
services:
  - type: web
    name: easymate-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

**Docker Compose**:
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
```

## Advantages & Benefits

### Framework Advantages

#### FastAPI
- **Performance**: Among the fastest Python web frameworks
- **Developer Experience**: Automatic interactive API documentation
- **Type Safety**: Built-in request/response validation
- **Modern Standards**: Native async/await, OpenAPI 3.0, JSON Schema
- **Easy Testing**: Excellent testing framework integration

#### Google Gemini Integration
- **Advanced AI**: State-of-the-art language model capabilities
- **Cost Effective**: Competitive pricing compared to alternatives
- **Streaming Support**: Real-time response generation
- **Reliability**: Google's enterprise-grade infrastructure
- **Flexibility**: Multiple model variants and configurations

#### Pydantic
- **Data Validation**: Automatic request/response validation
- **Type Conversion**: Seamless data type handling
- **Error Messages**: Clear, user-friendly validation errors
- **Performance**: Optimized validation engine
- **IDE Support**: Excellent autocomplete and type checking

### Architectural Benefits

#### Scalability
- **Async Architecture**: Handle thousands of concurrent requests
- **Stateless Design**: Easy horizontal scaling
- **Cloud Native**: Container-ready with health checks
- **Resource Efficient**: Minimal memory footprint

#### Maintainability
- **Clean Code Structure**: Well-organized, modular codebase
- **Type Safety**: Reduced runtime errors
- **Comprehensive Logging**: Easy debugging and monitoring
- **Documentation**: Auto-generated API docs

#### Security
- **Input Validation**: Automatic request sanitization
- **CORS Configuration**: Secure cross-origin handling
- **Error Handling**: No sensitive information leakage
- **Environment Management**: Secure configuration handling

#### Developer Experience
- **Fast Development**: Rapid prototyping and iteration
- **Interactive Docs**: Built-in API explorer
- **Hot Reloading**: Instant feedback during development
- **Type Hints**: Excellent IDE support and autocompletion

### Business Benefits

- **Rapid Deployment**: From development to production in minutes
- **Cost Effective**: Efficient resource utilization
- **Future Proof**: Modern technology stack with active development
- **Extensible**: Easy to add new features and integrations
- **Reliable**: Comprehensive error handling and monitoring

This architecture provides a solid foundation for building AI-powered applications with excellent performance, maintainability, and scalability characteristics.