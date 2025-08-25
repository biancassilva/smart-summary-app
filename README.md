# Smart Summary App - AI Text Summarization Platform

Smart Summary App is a modern, full-stack application that provides AI-powered text summarization with real-time streaming capabilities. Built with Next.js and FastAPI, it offers a seamless user experience for generating concise summaries from articles, meeting notes, emails, and other text content.

## 🚀 Features

### Frontend (Next.js + Tailwind CSS)

- **Modern UI**: Clean, responsive design with Tailwind CSS v4
- **Real-time Streaming**: Watch summaries generate in real-time
- **Character Validation**: Input validation with helpful feedback
- **Responsive Design**: Works perfectly on all devices
- **TypeScript**: Full type safety and better development experience

### Backend (FastAPI + Google Gemini)

- **FastAPI Framework**: High-performance, modern Python web framework
- **Google Gemini Integration**: Powered by Gemini 1.5 Flash for intelligent summarization
- **Server-Side Streaming**: Real-time summary generation with SSE
- **Word-by-Word Streaming**: Human-like typing animation for better UX
- **Comprehensive Logging**: Structured logging for monitoring and debugging
- **Health Monitoring**: Built-in health checks and monitoring
- **Scalable Architecture**: Designed for easy scaling and maintenance

## 🏗️ Architecture

```
smart-summary-app/
├── client/                 # Next.js Frontend
│   ├── src/app/           # App router components
│   ├── src/components/    # React components
│   ├── src/hooks/         # Custom React hooks
│   ├── src/lib/           # Utility libraries
│   ├── src/types/         # TypeScript type definitions
│   └── package.json       # Frontend dependencies
├── backend/               # FastAPI Backend
│   ├── app/               # Application code
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Configuration & utilities
│   │   ├── services/      # Business logic (Gemini service)
│   │   └── schemas/       # Data validation
│   └── requirements.txt   # Python dependencies
└── README.md              # This file
```

## 📋 Prerequisites

- **Node.js 18+** and npm
- **Python 3.8+** and pip
- **Google Gemini API Key** (required for AI summarization)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd smart-summary-app
```

### 2. Start the Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### 3. Start the Frontend

```bash
cd client

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Use the Application

1. Open `http://localhost:3000` in your browser
2. Paste your text (minimum 50 characters)
3. Click "Generate Summary"
4. Watch the summary generate in real-time!

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the backend directory with the following:

```bash
# Required
GEMINI_API_KEY=your-gemini-api-key-here

# Optional (with good defaults)
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_OUTPUT_TOKENS=8192
ENVIRONMENT=development
DEBUG=true
```

## 🐳 Docker Development

For easy development setup with Docker:

```bash
cd backend

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

## 📚 API Documentation

Once the backend is running, you can access:

- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/api/v1/health`

### Key Endpoints

- `POST /api/v1/chat/stream` - Streaming text summarization (Primary endpoint)
- `GET /api/v1/health` - Health check endpoint
- `GET /api/v1/health/ready` - Readiness probe
- `GET /api/v1/health/live` - Liveness probe

## 🔍 Testing

### Backend Tests

```bash
cd backend

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

### Frontend Tests

```bash
cd client

# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## 🚀 Production Deployment

### Backend Deployment

1. **Set Production Environment Variables**:

   ```bash
   ENVIRONMENT=production
   DEBUG=false
   GEMINI_API_KEY=your-production-gemini-key
   ALLOWED_ORIGINS=["https://yourdomain.com"]
   ```

2. **Use Production Server**:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Docker Deployment**:

   ```bash
   docker build -t smart-summary-backend .
   docker run -p 8000:8000 smart-summary-backend
   ```

### Frontend Deployment

1. **Build for Production**:

   ```bash
   npm run build
   ```

2. **Deploy to Vercel/Netlify** or serve the `out/` directory

## 🔒 Security Considerations

- **CORS**: Configure allowed origins in production
- **Rate Limiting**: Implement rate limiting for production use
- **Authentication**: Add JWT authentication for protected endpoints
- **HTTPS**: Always use HTTPS in production
- **API Keys**: Secure storage of Google Gemini API keys

## 📊 Monitoring

### Health Checks

- `/api/v1/health` - Quick health status
- `/api/v1/health/detailed` - Comprehensive health with dependencies

### Logging

The backend uses structured logging (JSON) for easy parsing and monitoring:

- **Request Logging**: All API requests and responses
- **Performance Metrics**: Request timing and database query metrics
- **Error Tracking**: Comprehensive error logging with context

## 🐛 Troubleshooting

### Common Issues

1. **Backend won't start**:

   - Check if `.env` file exists and has `GEMINI_API_KEY`
   - Ensure port 8000 is available
   - Verify virtual environment is activated
   - Check that all dependencies are installed

3. **Frontend can't connect to backend**:

   - Verify backend is running on port 8000
   - Check CORS configuration
   - Ensure no firewall blocking the connection

2. **Google Gemini API errors**:
   - Verify your Gemini API key is correct
   - Check API key has proper permissions
   - Ensure you're not hitting rate limits
   - Verify you have access to Gemini 1.5 Flash model

### Getting Help

- Check the logs in the backend terminal
- Review the API documentation at `http://localhost:8000/docs`
- Check the health endpoint at `http://localhost:8000/api/v1/health`
- See the backend README for detailed configuration options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent Python web framework
- **Next.js** for the powerful React framework
- **Google Gemini** for the AI capabilities
- **Tailwind CSS** for the beautiful UI components

---

**Happy Summarizing! 🎉**
