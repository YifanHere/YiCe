# YiCe - AI-Powered Code Review Assistant

YiCe is an intelligent code review tool that leverages AI to help developers improve code quality through automated analysis and actionable suggestions.

## Features

### Core AI Code Review
- AI-driven code review and suggestions
- Fast and scalable backend
- Modern, intuitive frontend interface
- Easy to set up and use

### Phase 2: Financial Data Integration
- **Multi-source data providers**: Tushare Pro API integration with extensible provider architecture
- **Comprehensive financial data**: K-line data (daily/weekly/monthly), fundamental data, and macro-economic indicators
- **Advanced technical analysis**: 30+ technical indicators (trend, momentum, volume, volatility) via pandas-ta-classic
- **Intelligent caching system**: Redis caching with automatic fallback to local file cache
- **Custom indicators**: User-defined technical indicators with Python expression support
- **Rate limiting & resilience**: Built-in rate limiting, retry mechanisms, and error handling

## Tech Stack

### Backend
- **FastAPI**: Modern web framework for building APIs
- **LangGraph**: Framework for building stateful AI applications
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI
- **Python 3.11+**

### Data Layer (Phase 2)
- **Tushare Pro**: Professional financial data API for Chinese markets
- **pandas-ta-classic**: Technical analysis library with 30+ indicators
- **Redis**: In-memory caching for high-performance data access
- **pandas**: Data manipulation and analysis
- **Tenacity**: Retry library for robust external API calls

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

### Using the Data Layer (Phase 2)

YiCe now includes a comprehensive financial data layer for technical analysis. To start using Phase 2 features:

1. **Configure Tushare Token**: Add your Tushare Pro token to `backend/.env`:
   ```bash
   TUSHARE_TOKEN=your_token_here
   ```

2. **Optional Redis Setup**: For caching, set up Redis or use file-based fallback.

3. **Explore Documentation**:
   - See [Data Layer Architecture](docs/data_layer_architecture.md) for architecture details
   - Check [API Usage Examples](docs/api_usage.md) for code examples
   - Review [Technical Indicators List](docs/indicators_list.md) for available indicators

4. **Example - Get K-line Data**:
   ```python
   from app.services.kline_service import KlineDataService
   import asyncio
   
   async def example():
       service = KlineDataService()
       data = await service.get_daily_kline("000001.SZ")
       print(f"Fetched {len(data)} records")
   
   asyncio.run(example())
   ```

## Documentation

### Core Documentation
- [Architecture Guide](docs/architecture.md)
- [Quick Start Guide](docs/quickstart.md)

### Phase 2: Data Layer Documentation
- [Data Layer Architecture](docs/data_layer_architecture.md) - Architecture of financial data providers, services, and caching
- [API Usage Examples](docs/api_usage.md) - Code examples for K-line data, indicators, and custom indicators
- [Technical Indicators List](docs/indicators_list.md) - Complete list of 30+ supported technical indicators

## License

MIT License
