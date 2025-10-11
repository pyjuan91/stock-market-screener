# Stock Market Screener - Backend

Python backend for the Stock Market Screener application, featuring FastAPI, FinBERT sentiment analysis, and strategy backtesting.

## Setup

### Requirements
- Python 3.13+
- Poetry for dependency management

### Installation

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys:
# - NEWS_API_KEY (get free key at https://newsapi.org/)
# - FINNHUB_API_KEY (optional, from https://finnhub.io/)
```

3. Run the development server:
```bash
poetry shell
python api.py
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

**Note:** First run will download the FinBERT model (~440MB), which may take a few minutes.

## Project Structure

```
backend/
├── api.py                      # FastAPI application & routes
├── stock_screener/             # Stock analysis module
│   ├── screener.py            # Main analysis orchestrator
│   ├── data_fetcher.py        # Yahoo Finance data fetching
│   └── indicator_calculator.py # Technical indicator calculations
├── ml_models/                  # ML/AI models
│   └── sentiment_analyzer.py  # FinBERT sentiment analysis
├── data_sources/               # External data sources
│   └── news_fetcher.py        # News API integration
├── backtesting/                # Backtesting engine
│   ├── strategy_engine.py     # Core backtesting framework
│   ├── performance_metrics.py # Performance calculation (Sharpe, etc.)
│   └── advanced_strategies.py # ML-enhanced trading strategies
├── pyproject.toml              # Dependencies & project config
└── .env.example                # Environment variables template
```

## API Endpoints

### Stock Analysis
- `GET /` - Health check
- `POST /api/scan` - Analyze multiple tickers with technical indicators
- `GET /api/history/{ticker}` - Get historical data with indicators

### Sentiment Analysis
- `GET /api/sentiment/{ticker}` - Get sentiment analysis for a ticker
- `POST /api/sentiment/batch` - Analyze sentiment for multiple tickers

### Backtesting
- `POST /api/backtest` - Run strategy backtest
- `POST /api/backtest/compare` - Compare multiple strategies

Full API documentation available at `/docs` when running the server.

## Technologies

- **FastAPI** - Modern, fast web framework
- **FinBERT (Transformers)** - Financial sentiment analysis ML model
- **PyTorch** - Deep learning framework
- **yfinance** - Stock data fetching
- **pandas & NumPy** - Data manipulation
- **pandas-ta** - Technical indicators
- **Poetry** - Dependency management

## Development

### Running Tests
```bash
poetry run pytest
```

### Building for Production
```bash
poetry build
```

## Deployment

The backend is configured for easy deployment on platforms like Render.com:

- Build command: `poetry install`
- Start command: `python api.py`
- Environment variables: Set `NEWS_API_KEY`, `FINNHUB_API_KEY`, `FRONTEND_URL`, `RENDER_EXTERNAL_URL`

## License

MIT License - See parent directory LICENSE file.
