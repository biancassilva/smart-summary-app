# Smart Summary App - AI Text Summarization Platform

Smart Summary App is a modern, full-stack application that provides AI-powered text summarization with real-time streaming capabilities. Built with Next.js and FastAPI, it offers a seamless user experience for generating concise summaries from articles, meeting notes, emails, and other text content.

## 🚀 Features

### Frontend (Next.js + Tailwind CSS)

- **Modern UI**: Clean, responsive design with Tailwind CSS v4
- **Real-time Streaming**: Watch summaries generate in real-time
- **Character Validation**: Input validation with helpful feedback
- **Responsive Design**: Works perfectly on all devices
- **TypeScript**: Full type safety and better development experience

### Backend (FastAPI + OpenAI)

- **FastAPI Framework**: High-performance, modern Python web framework
- **OpenAI Integration**: Powered by GPT-4 for intelligent summarization
- **Server-Side Streaming**: Real-time summary generation with SSE
- **SQLite Development**: Easy setup with SQLite (PostgreSQL for production)
- **Comprehensive Logging**: Structured logging with structlog
- **Health Monitoring**: Built-in health checks and monitoring
- **Scalable Architecture**: Designed for easy scaling and maintenance

## 🏗️ Architecture

```
easymate/
├── client/                 # Next.js Frontend
│   ├── src/app/           # App router components
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
├── backend/               # FastAPI Backend
│   ├── app/               # Application code
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Configuration & utilities
│   │   ├── db/            # Database models & connections
│   │   ├── services/      # Business logic
│   │   └── schemas/       # Data validation
│   ├── tests/             # Test suite
│   ├── install.sh         # Easy installation script
│   └── start.sh           # Startup script
└── README.md              # This file
```

## 📋 Prerequisites

- **Node.js 18+** and npm
- **Python 3.8+** and pip
- **OpenAI API Key** (required for summarization)
- **PostgreSQL** (optional, for production only)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd easymate
```

### 2. Start the Backend (Easy Installation)

```bash
cd backend

# Run the easy installation script (avoids compilation issues)
./install.sh

# Start the backend
./start.sh
```

The backend will be available at `http://localhost:8000`

**What the installation script does:**

- Creates a virtual environment
- Installs dependencies step by step (avoiding problematic packages)
- Uses SQLite for easy development (no database setup required)
- Guides you through configuration

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

The installation script will create a `.env` file automatically. You just need to add your OpenAI API key:

```bash
# Required
OPENAI_API_KEY=your-openai-api-key-here

# Optional (with good defaults)
DEBUG=false
HOST=0.0.0.0
PORT=8000
USE_SQLITE=true  # Uses SQLite for easy development
```

### Database Configuration

**Development (Default)**: SQLite

- No installation required
- No compilation issues
- File-based database
- Perfect for development

**Production**: PostgreSQL

- Set `USE_SQLITE=false` in `.env`
- Update `DATABASE_URL` to your PostgreSQL connection string

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

- `POST /api/v1/summaries/stream` - Create summary for streaming
- `GET /api/v1/summaries/{id}/stream` - Stream summary generation
- `GET /api/v1/summaries/{id}` - Get summary by ID
- `GET /api/v1/summaries/` - List all summaries

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
   DEBUG=false
   USE_SQLITE=false
   DATABASE_URL=your-production-db-url
   SECRET_KEY=your-production-secret-key
   ```

2. **Use Production Server**:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Docker Deployment**:

   ```bash
   docker build -t easymate-backend .
   docker run -p 8000:8000 easymate-backend
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
- **API Keys**: Secure storage of OpenAI API keys

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

1. **Installation compilation errors**:

   - Use `./install.sh` instead of `pip install -r requirements.txt`
   - This avoids problematic packages like `asyncpg`

2. **Backend won't start**:

   - Check if `.env` file exists and has required variables
   - Ensure port 8000 is available
   - Run `./install.sh` first if virtual environment is missing

3. **Frontend can't connect to backend**:

   - Verify backend is running on port 8000
   - Check CORS configuration
   - Ensure no firewall blocking the connection

4. **OpenAI API errors**:
   - Verify your API key is correct
   - Check API key has sufficient credits
   - Ensure you're not hitting rate limits

### Getting Help

- Check the logs in the backend terminal
- Review the API documentation at `/docs`
- Check the health endpoint for system status
- See `backend/TROUBLESHOOTING.md` for detailed solutions

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
- **OpenAI** for the AI capabilities
- **Tailwind CSS** for the beautiful UI components

---

**Happy Summarizing! 🎉**
