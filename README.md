# Stock Market Screener with ML Sentiment Analysis & Backtesting

An advanced full-stack stock analysis platform combining **technical indicators**, **ML-powered sentiment analysis (FinBERT)**, and **strategy backtesting**. Built with Python FastAPI backend and React frontend, featuring a clean Apple-inspired design.

<img width="1920" height="2300" alt="screenshot-rocks" src="https://github.com/user-attachments/assets/33bdfdcb-9da0-498f-a347-f51194629e16" />




## What It Does

### 🎯 Stock Analysis
- Real-time and historical stock data fetching
- Technical indicators: RSI, MACD, Bollinger Bands, Moving Averages (MA20, MA50)
- Multi-ticker analysis support
- Interactive charts with technical overlays

### 🤖 AI-Powered Sentiment Analysis
- **FinBERT sentiment model** for financial news analysis
- Multi-source news aggregation (NewsAPI, Finnhub)
- Sentiment scoring: -1 (bearish) to +1 (bullish)
- Article-level and aggregate sentiment metrics
- Confidence scores and sentiment distribution

### 📊 Strategy Backtesting Engine
- Test trading strategies on historical data (1mo to 5 years)
- **7 Built-in strategies:**
  - Simple: RSI, MACD, MA Crossover
  - ML-Enhanced: RSI+Sentiment, MACD+Sentiment, Multi-Indicator, Momentum+Sentiment
- **Performance metrics:**
  - Sharpe Ratio & Sortino Ratio
  - Maximum Drawdown
  - Win Rate & Profit Factor
  - Risk-adjusted returns
- Strategy comparison and ranking
- Trade-by-trade analysis with equity curves

### 💡 User Experience
- Clean, Apple-inspired interface
- Responsive design (desktop & mobile)
- Keyboard shortcuts (Enter to analyze)
- Real-time loading states
- Smart backend sleep detection with cached fallbacks

## Live Demo

The app is deployed on Render.com: https://stock-frontend-1yd4.onrender.com/

*Note: If it's the first request in a while, the backend might take 30-60 seconds to wake up. That's just how Render's free tier works. The app handles this with cached data so demos still look smooth.*

## Tech Stack

**Backend:**
- Python 3.13+
- **FastAPI** - Modern web framework
- **FinBERT (Transformers)** - Financial sentiment analysis ML model
- **PyTorch** - Deep learning framework
- **yfinance** - Stock data fetching
- **pandas & NumPy** - Data manipulation
- **pandas-ta** - Technical indicators
- Poetry for dependency management

**Frontend:**
- React 19+
- Material-UI v7 - UI components
- Recharts - Interactive charts
- Axios - API client

**ML & Data:**
- ProsusAI/finbert - Pre-trained financial sentiment model
- NewsAPI & Finnhub - News data sources
- Custom backtesting engine with performance metrics

## Getting Started

**Requirements:** Python 3.13+, Node.js 16+, Poetry

### Backend Setup

1. Clone and install dependencies:

```bash
git clone https://github.com/pyjuan91/stock-market-screener.git
cd stock-market-screener
poetry install
```

2. Set up environment variables (optional but recommended):

```bash
cp .env.example .env
# Edit .env and add your API keys:
# - NEWS_API_KEY (get free key at https://newsapi.org/)
# - FINNHUB_API_KEY (optional, from https://finnhub.io/)
```

3. Start the backend:

```bash
poetry shell
python api.py
```

Backend will be at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`

**Note:** First run will download the FinBERT model (~440MB), which may take a few minutes.

### Frontend Setup

In a new terminal, get the frontend going:

```bash
cd frontend
npm install
npm start
```

Frontend will be at `http://localhost:3000`

## Building for Production

**Backend:**
```bash
poetry build
```

**Frontend:**
```bash
cd frontend
npm run build
```

## Deploying to Render

This thing is set up to work well with Render.com:

**Backend deployment:**
- Connect your GitHub repo to Render
- Choose "Web Service"
- Build command: `poetry install`
- Start command: `python api.py`

**Frontend deployment:**
- Choose "Static Site"
- Build command: `cd frontend && npm install && npm run build`
- Publish directory: `frontend/build`
- Environment variable: `REACT_APP_API_URL=https://your-backend-url.onrender.com`

### Environment Variables

**Backend:**
- `NEWS_API_KEY` - NewsAPI key for news fetching (optional, has fallback demo data)
- `FINNHUB_API_KEY` - Finnhub API key (optional)
- `PORT` - Server port (Render sets automatically)
- `FRONTEND_URL` - Production frontend URL for CORS
- `RENDER_EXTERNAL_URL` - Render backend URL for CORS

**Frontend:**
- `REACT_APP_API_URL` - Backend API URL for production

## API Endpoints

### Stock Analysis
- **GET /** - Health check
- **POST /api/scan** - Analyze multiple tickers with technical indicators
  ```json
  {
    "tickers": ["AAPL", "GOOG", "MSFT"]
  }
  ```
- **GET /api/history/{ticker}** - Get historical data with indicators

### Sentiment Analysis
- **GET /api/sentiment/{ticker}** - Get sentiment analysis for a ticker
  - Query params: `days` (default: 7), `max_articles` (default: 20)
  - Returns: Overall sentiment score, confidence, article breakdown

- **POST /api/sentiment/batch** - Analyze sentiment for multiple tickers
  ```json
  {
    "tickers": ["AAPL", "TSLA", "NVDA"],
    "days": 7
  }
  ```

### Backtesting
- **POST /api/backtest** - Run strategy backtest
  ```json
  {
    "ticker": "AAPL",
    "strategy": "rsi",
    "period": "1y",
    "interval": "1d",
    "initial_capital": 10000
  }
  ```
  - Available strategies: `rsi`, `macd`, `ma_crossover`, `rsi_sentiment`, `macd_sentiment`, `multi_indicator_sentiment`, `momentum_sentiment`

- **POST /api/backtest/compare** - Compare multiple strategies
  ```json
  {
    "ticker": "AAPL",
    "strategies": ["rsi", "macd", "rsi_sentiment"],
    "period": "1y"
  }
  ```

**Interactive API docs:** `http://localhost:8000/docs`

## How to Use

### Basic Stock Analysis
1. Enter stock ticker symbols (e.g., AAPL, GOOG, MSFT)
2. Press Enter or click "Analyze"
3. View technical indicators in the results table
4. Click any row to see detailed historical charts

### Sentiment Analysis (API)
```bash
# Get sentiment for a single stock
curl http://localhost:8000/api/sentiment/AAPL

# Returns sentiment score, news articles, confidence
```

### Backtesting (API)
```bash
# Backtest RSI strategy
curl -X POST http://localhost:8000/api/backtest \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","strategy":"rsi","period":"1y"}'

# Compare strategies
curl -X POST http://localhost:8000/api/backtest/compare \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","strategies":["rsi","macd","rsi_sentiment"],"period":"1y"}'
```

## Project Structure

```
stock-market-screener/
├── api.py                      # FastAPI application
├── stock_screener/             # Stock analysis module
│   ├── screener.py            # Main analysis orchestrator
│   ├── data_fetcher.py        # Yahoo Finance data
│   └── indicator_calculator.py # Technical indicators
├── ml_models/                  # ML/AI models
│   └── sentiment_analyzer.py  # FinBERT sentiment analysis
├── data_sources/               # External data sources
│   └── news_fetcher.py        # News API integration
├── backtesting/                # Backtesting engine
│   ├── strategy_engine.py     # Core backtesting logic
│   ├── performance_metrics.py # Sharpe, drawdown, etc.
│   └── advanced_strategies.py # ML-enhanced strategies
└── frontend/                   # React application
    └── src/
        └── App.js             # Main UI component
```

## What's Next

### Potential Enhancements
- **Deep Learning:** LSTM/GRU models for price prediction
- **Real-time:** WebSocket integration for live price updates
- **Database:** PostgreSQL for historical sentiment/backtest storage
- **Frontend:** Sentiment dashboard + backtesting visualization UI
- **Portfolio:** Multi-asset portfolio optimization
- **Alerts:** Price/sentiment-based notification system
- **Testing:** Comprehensive unit/integration test suite
- **Docker:** Containerization for easy deployment

## Contributing

Feel free to fork the repo and submit pull requests. The usual GitHub workflow applies:

1. Fork it
2. Create your feature branch (`git checkout -b feature/cool-feature`)
3. Commit your changes (`git commit -m 'Add cool feature'`)
4. Push to the branch (`git push origin feature/cool-feature`)
5. Open a Pull Request

## License

MIT License - do whatever you want with it.
