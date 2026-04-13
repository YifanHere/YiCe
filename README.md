# YiCe - AI-Powered Code Review Assistant

YiCe is an intelligent code review tool that leverages AI to help developers improve code quality through automated analysis and actionable suggestions.

## Features

- AI-driven code review and suggestions
- Fast and scalable backend
- Modern, intuitive frontend interface
- Easy to set up and use

## Tech Stack

### Backend
- **FastAPI**: Modern web framework for building APIs
- **LangGraph**: Framework for building stateful AI applications
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI
- **Python 3.11+**

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **TypeScript**: Type-safe development
- **Vite**: Next-generation frontend tooling
- **Pinia**: State management for Vue
- **Vue Router**: Official router for Vue

## Quick Start

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup
```bash
cd backend
# Install dependencies (using uv or pip)
uv pip install -r pyproject.toml
# Copy environment file
cp .env.example .env
# Start server
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
# Install dependencies
npm install
# Copy environment file
cp .env.example .env
# Start development server
npm run dev
```

## Documentation

- [Architecture Guide](docs/architecture.md)
- [Quick Start Guide](docs/quickstart.md)

## License

MIT License
