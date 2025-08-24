# EasyMate Backend API

A scalable, production-ready text summarization API built with FastAPI, PostgreSQL, Redis, and OpenAI. The API provides asynchronous text summarization capabilities with comprehensive monitoring, rate limiting, and security features.

## 🚀 Features

- **Text Summarization**: AI-powered text summarization using OpenAI GPT models
- **Asynchronous Processing**: Background task processing with Celery
- **RESTful API**: Clean REST endpoints with OpenAPI documentation
- **Database Persistence**: PostgreSQL storage with SQLAlchemy ORM
- **Caching**: Redis-based caching and session management
- **Security**: JWT authentication, rate limiting, and CORS protection
- **Monitoring**: Prometheus metrics and structured logging
- **Scalability**: Horizontal scaling support with load balancing

## 🏗️ Architecture

### Core Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   PostgreSQL    │    │      Redis      │
│                 │    │   Database      │    │   Cache/Queue   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Celery       │    │   OpenAI API    │    │   Monitoring    │
│   Workers      │    │   Integration   │    │   & Logging     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Cache/Queue**: Redis 5.0
- **Task Queue**: Celery 5.3
- **AI Service**: OpenAI API
- **Authentication**: JWT with python-jose
- **Monitoring**: Prometheus metrics
- **Logging**: Structured logging with structlog

### Key Assumptions

1. **Async-First**: Built with async/await patterns for high concurrency
2. **Microservices Ready**: Designed for containerization and horizontal scaling
3. **Event-Driven**: Uses background tasks for long-running operations
4. **Stateless**: API instances can be scaled horizontally
5. **Database-First**: PostgreSQL as the primary data store

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- OpenAI API key

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# API Settings
DEBUG=false
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/easymate
DATABASE_URL_TEST=postgresql://user:password@localhost:5432/easymate_test

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.3

# Security
ALLOWED_HOSTS=["*"]
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=100
```

### Installation

1. **Clone the repository and navigate to backend:**

   ```bash
   cd backend
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**

   ```bash
   # Create database
   createdb easymate

   # Run migrations (if using Alembic)
   alembic upgrade head
   ```

5. **Start Redis:**

   ```bash
   redis-server
   ```

6. **Start Celery worker (in a separate terminal):**

   ```bash
   celery -A app.celery_app worker --loglevel=info
   ```

7. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Setup (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📚 API Documentation

Once running, access the API documentation at:

- **Swagger UI**: `http://localhost:8000/api/v1/docs`
- **ReDoc**: `http://localhost:8000/api/v1/redoc`
- **OpenAPI JSON**: `http://localhost:8000/api/v1/openapi.json`

### Key Endpoints

- `POST /api/v1/summaries/` - Create a new summary request
- `GET /api/v1/summaries/{id}` - Get summary by ID
- `GET /api/v1/summaries/` - List summaries with pagination
- `GET /api/v1/health` - Health check endpoint

## 🔮 Future Improvements

### Short-term (1-3 months)

- **User Authentication**: Implement JWT-based user management
- **File Upload Support**: Accept PDF, DOCX, and TXT files
- **Batch Processing**: Process multiple documents simultaneously
- **Summary Templates**: Customizable summary formats and styles
- **Webhook Support**: Notify external systems of completion

### Medium-term (3-6 months)

- **Multi-language Support**: Summarization in multiple languages
- **Advanced AI Models**: Support for GPT-4, Claude, and other models
- **Content Analysis**: Extract key topics, sentiment, and entities
- **API Versioning**: Proper API versioning strategy
- **GraphQL Support**: Alternative to REST endpoints

### Long-term (6+ months)

- **Real-time Processing**: WebSocket support for live updates
- **Custom Training**: Fine-tune models on domain-specific data
- **Analytics Dashboard**: Usage metrics and insights
- **Multi-tenant Support**: SaaS-ready architecture
- **Edge Computing**: Deploy models closer to users

## 🚀 Scaling Considerations

### Horizontal Scaling

- **Load Balancer**: Use Nginx or HAProxy for traffic distribution
- **Multiple API Instances**: Deploy multiple FastAPI instances
- **Database Sharding**: Partition data across multiple databases
- **Redis Cluster**: Distribute cache across multiple Redis nodes

### Performance Optimization

- **Connection Pooling**: Optimize database and Redis connections
- **Caching Strategy**: Implement multi-level caching (Redis + in-memory)
- **Async Processing**: Use Celery for CPU-intensive tasks
- **CDN Integration**: Serve static content through CDN

### Infrastructure

- **Container Orchestration**: Kubernetes for container management
- **Auto-scaling**: Implement auto-scaling based on metrics
- **Monitoring**: Prometheus + Grafana for observability
- **Log Aggregation**: Centralized logging with ELK stack

## 🔒 Security Considerations

### Authentication & Authorization

- **JWT Tokens**: Secure token-based authentication
- **Role-based Access**: Implement user roles and permissions
- **API Keys**: Support for API key authentication
- **OAuth Integration**: Third-party authentication providers

### Data Protection

- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: Prevent abuse and DDoS attacks
- **CORS Configuration**: Restrict cross-origin requests
- **SQL Injection Protection**: Use parameterized queries

### Infrastructure Security

- **HTTPS Only**: Enforce TLS encryption
- **Secrets Management**: Secure environment variable handling
- **Network Security**: VPC and firewall configuration
- **Regular Updates**: Keep dependencies updated

### Compliance

- **GDPR Compliance**: Data privacy and right to deletion
- **SOC 2**: Security and availability controls
- **Data Encryption**: Encrypt data at rest and in transit
- **Audit Logging**: Comprehensive activity logging

## 📊 Monitoring & Observability

### Metrics

- **Application Metrics**: Request rate, response time, error rate
- **Business Metrics**: Summary creation rate, processing time
- **Infrastructure Metrics**: CPU, memory, disk usage
- **Custom Metrics**: OpenAI API usage, cost tracking

### Logging

- **Structured Logging**: JSON-formatted logs for easy parsing
- **Log Levels**: Configurable logging levels
- **Correlation IDs**: Track requests across services
- **Centralized Logging**: Aggregate logs for analysis

### Alerting

- **Error Rate Alerts**: Notify on high error rates
- **Performance Alerts**: Alert on slow response times
- **Infrastructure Alerts**: Monitor system resources
- **Business Alerts**: Track API usage and costs

## 🧪 Testing

### Test Types

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and database operations
- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Load testing and stress testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_summary_service.py
```

## 📦 Deployment

### Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] SSL certificates installed
- [ ] Monitoring configured
- [ ] Backup strategy implemented
- [ ] CI/CD pipeline set up
- [ ] Load balancer configured
- [ ] Auto-scaling policies defined

### Deployment Options

- **Cloud Platforms**: AWS, GCP, Azure
- **Container Platforms**: Docker, Kubernetes
- **Serverless**: AWS Lambda, Google Cloud Functions
- **Traditional**: VPS, dedicated servers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the API documentation
- Review the logs for error details
- Contact the development team

---

**Note**: This is a production-ready backend API designed for scalability and security. Always review security configurations and follow best practices for your specific deployment environment.

