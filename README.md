# Stock Market Screener

A full-stack web app for analyzing stock market data with technical indicators and interactive charts. Built with Python FastAPI backend and React frontend, featuring a clean Apple-inspired design.

## Screenshots

<!-- Add your screenshots here -->
*Screenshots will be added soon*

## What It Does

### Stock Analysis
- Fetches real-time stock data and historical information
- Calculates technical indicators: RSI, MACD, and moving averages (MA20, MA50)
- Supports analyzing multiple stocks at once
- Interactive charts with technical overlays

### User Experience
- Clean, Apple-inspired interface that's easy on the eyes
- Works well on both desktop and mobile
- Press Enter to trigger analysis (because who doesn't love keyboard shortcuts)
- Real-time loading states so you know something's happening

### Smart Backend Handling
- Detects when Render.com backend is sleeping and shows a helpful dialog
- Falls back to cached demo data for popular stocks when backend is unavailable
- Handles timeout scenarios gracefully for better demo experience

### Technical Stuff
- FastAPI backend that's pretty fast
- React frontend with Material-UI components
- CORS properly configured
- Environment-based config for easy deployment

## Live Demo

The app is deployed on Render.com: [Your Render URL Here]

*Note: If it's the first request in a while, the backend might take 30-60 seconds to wake up. That's just how Render's free tier works. The app handles this with cached data so demos still look smooth.*

## Tech Stack

**Backend:**
- Python 3.8+
- FastAPI for the web framework
- Poetry for dependency management
- yfinance for stock data
- pandas for data manipulation
- TA-Lib for technical analysis

**Frontend:**
- React 19+
- Material-UI for components
- Recharts for charts
- Axios for API calls

## Getting Started

You'll need Python 3.8+, Node.js 16+, and Poetry installed.

### Backend Setup

Clone the repo and get the backend running:

```bash
git clone https://github.com/pyjuan91/stock-market-screener.git
cd stock-market-screener
poetry install
poetry shell
python api.py
```

Backend will be at `http://localhost:8000` and API docs at `http://localhost:8000/docs`

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
- `PORT` - Server port (Render sets this automatically)
- `CORS_ORIGINS` - Allowed CORS origins

**Frontend:**
- `REACT_APP_API_URL` - Your backend URL for production

## API Endpoints

**GET /** - Basic health check

**POST /api/scan** - Analyze stocks
```json
{
  "tickers": ["AAPL", "GOOG", "MSFT"]
}
```

**GET /api/history/{ticker}** - Get historical data for a stock

## How to Use

1. Type in some stock symbols (like AAPL, GOOG, MSFT)
2. Hit Analyze or just press Enter
3. Check out the results in the table
4. Click any row to see detailed charts
5. If the backend is sleeping, you can wait or use cached demo data

## What's Next

### More Analytics
- Additional technical indicators (Bollinger Bands, Stochastic Oscillator)
- Portfolio tracking and performance analysis
- Real-time price updates with WebSocket
- Price alerts and notifications

### UI Improvements
- Dark mode toggle
- Customizable chart themes
- Better filtering and sorting
- Stock comparison tools

### Data & Features
- Fundamental analysis (P/E ratio, market cap, etc.)
- News sentiment analysis
- Export functionality (PDF reports, CSV data)
- Historical backtesting

### Technical Enhancements
- Database integration for persistence
- User authentication and watchlists
- API rate limiting and caching
- Proper testing suite
- Docker containerization

### Performance & Deployment
- CDN integration
- Server-side rendering support
- Progressive Web App features
- Better monitoring and analytics

## Contributing

Feel free to fork the repo and submit pull requests. The usual GitHub workflow applies:

1. Fork it
2. Create your feature branch (`git checkout -b feature/cool-feature`)
3. Commit your changes (`git commit -m 'Add cool feature'`)
4. Push to the branch (`git push origin feature/cool-feature`)
5. Open a Pull Request

## License

MIT License - do whatever you want with it.