# Stock Market Screener

A modern, full-stack web application for analyzing US stock market data with real-time technical indicators and interactive visualizations. Built with a Python FastAPI backend and React frontend, featuring a clean Apple-inspired design.

## 🖼️ Screenshots

<!-- Add your screenshots here -->
*Screenshots will be added soon*

## ✨ Features

### 📊 Technical Analysis
- **Real-time stock data** - Fetch current stock prices and historical data
- **Technical indicators** - RSI, MACD, Moving Averages (MA20, MA50)
- **Interactive charts** - Historical price charts with technical overlays
- **Multi-stock analysis** - Analyze multiple stocks simultaneously

### 🎨 Modern UI/UX
- **Apple-inspired design** - Clean, minimalist interface with Apple's design principles
- **Responsive layout** - Works seamlessly on desktop and mobile devices
- **Real-time feedback** - Loading states and interactive hover effects
- **Keyboard shortcuts** - Press Enter to trigger analysis

### 🚀 Smart Deployment Features
- **Timeout handling** - Intelligent detection of sleeping backend services
- **Cache fallback** - Cached demo data for popular stocks when backend is unavailable
- **Render.com optimization** - Built-in handling for cold start delays on Render.com

### 🛠️ Technical Features
- **FastAPI backend** - High-performance async Python API
- **React frontend** - Modern React with Material-UI components
- **CORS enabled** - Properly configured for cross-origin requests
- **Environment-based configuration** - Seamless development to production deployment

## 🚀 Live Demo

The application is deployed on Render.com and available at: [Your Render URL Here]

*Note: The backend may take 30-60 seconds to wake up on first request due to Render's free tier limitations. The app includes intelligent cache fallback for a smooth demo experience.*

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern, fast web framework
- **Poetry** - Dependency management
- **yfinance** - Stock data fetching
- **pandas** - Data manipulation
- **TA-Lib** - Technical analysis library

### Frontend
- **React 19+**
- **Material-UI** - React component library
- **Recharts** - Chart visualization library
- **Axios** - HTTP client

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Poetry (see [official installation instructions](https://python-poetry.org/docs/#installation))
- npm or yarn

## 🔧 Local Development Setup

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pyjuan91/stock-market-screener.git
   cd stock-market-screener
   ```

2. **Install Python dependencies:**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment:**
   ```bash
   poetry shell
   ```

4. **Start the backend server:**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## 🏗️ Build for Production

### Backend Build
```bash
cd backend
poetry build
```

### Frontend Build
```bash
cd frontend
npm run build
```

## 🌐 Deployment

### Render.com Deployment

This project is optimized for deployment on Render.com:

1. **Backend deployment:**
   - Connect your GitHub repository to Render
   - Choose "Web Service"
   - Set build command: `poetry install`
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Set environment variables as needed

2. **Frontend deployment:**
   - Choose "Static Site"
   - Set build command: `cd frontend && npm install && npm run build`
   - Set publish directory: `frontend/build`
   - Set environment variable: `REACT_APP_API_URL=https://your-backend-url.onrender.com`

### Environment Variables

#### Backend
- `PORT` - Server port (automatically set by Render)
- `CORS_ORIGINS` - Allowed CORS origins

#### Frontend
- `REACT_APP_API_URL` - Backend API URL for production

## 📝 API Endpoints

### GET `/`
Health check endpoint

### POST `/api/scan`
Analyze stocks with technical indicators
```json
{
  "tickers": ["AAPL", "GOOG", "MSFT"]
}
```

### GET `/api/history/{ticker}`
Get historical data for a specific stock

## 🎯 Usage

1. **Enter stock tickers** - Input one or more stock symbols (e.g., AAPL, GOOG, MSFT)
2. **Click Analyze or press Enter** - Trigger the analysis
3. **View results** - See technical indicators in a clean table format
4. **Explore charts** - Click on any stock row to view detailed historical charts
5. **Handle timeouts** - If backend is sleeping, choose to wait or use cached demo data

## 🔮 Future Work

### 📈 Enhanced Analytics
- [ ] Additional technical indicators (Bollinger Bands, Stochastic Oscillator)
- [ ] Portfolio tracking and performance analysis
- [ ] Real-time price updates with WebSocket integration
- [ ] Price alerts and notifications

### 🎨 UI/UX Improvements
- [ ] Dark mode toggle
- [ ] Customizable chart themes
- [ ] Advanced filtering and sorting options
- [ ] Stock comparison tools

### 📊 Data & Features
- [ ] Fundamental analysis metrics (P/E ratio, market cap, etc.)
- [ ] News sentiment analysis integration
- [ ] Export functionality (PDF reports, CSV data)
- [ ] Historical backtesting capabilities

### 🔧 Technical Enhancements
- [ ] Database integration for data persistence
- [ ] User authentication and personalized watchlists
- [ ] API rate limiting and caching
- [ ] Automated testing suite
- [ ] Docker containerization

### 🌐 Deployment & Performance
- [ ] CDN integration for faster loading
- [ ] Server-side rendering (SSR) support
- [ ] Progressive Web App (PWA) features
- [ ] Advanced monitoring and analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for stock data access
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python web framework
- [Material-UI](https://mui.com/) for beautiful React components
- [Recharts](https://recharts.org/) for interactive chart components
- [Render.com](https://render.com/) for reliable hosting platform

---

⭐ **Star this repository if you find it helpful!**