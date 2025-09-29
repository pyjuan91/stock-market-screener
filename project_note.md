# Claude Project Notes - Stock Market Screener

**Last Updated:** 2025-09-28 23:05:00
**Project Owner:** Po-Yu Juan (pyjuan91@gmail.com)
**Deployment:** Render.com (production)

## Project Overview
A full-stack stock market analysis tool with Python backend and React frontend that fetches, analyzes, and visualizes stock data with technical indicators.

## Architecture
- **Backend:** FastAPI (Python 3.13+) with uvicorn
- **Frontend:** React 19.1.1 with Material-UI
- **Data Source:** Yahoo Finance (yfinance)
- **Deployment:** Render.com (no Vercel configs present)
- **Dependency Management:** Poetry

## Key Components

### Backend (`/`)
- `main.py` - CLI interface for stock analysis with argparse
- `api.py` - FastAPI REST API with CORS setup for Render deployment
- `stock_screener/` - Core analysis module
  - `screener.py` - Main analysis orchestrator
  - `data_fetcher.py` - Yahoo Finance data retrieval
  - `indicator_calculator.py` - Technical indicators (MACD, RSI, MA, Bollinger)
- `requirements.txt` - Pip dependencies (minimal)
- `pyproject.toml` - Poetry configuration with FastAPI, yfinance, pandas-ta

### Frontend (`/frontend/`)
- React app with Material-UI components
- Package.json includes: React 19, MUI, axios, recharts
- Standard CRA structure in `src/`

## API Endpoints
- `GET /` - Welcome message
- `POST /api/scan` - Analyze multiple tickers with technical indicators
- `GET /api/history/{ticker}` - Historical analysis for single ticker

## Technical Indicators Supported
- MACD (Moving Average Convergence Divergence)
- RSI (Relative Strength Index)
- Moving Averages
- Bollinger Bands

## Development Environment
- Python 3.13+ required
- Poetry for dependency management
- React development server on port 3000
- FastAPI server on port 8000

## Current State
- Vercel deployment files removed (as of 2025-09-28)
- Configured for Render.com deployment
- CORS properly configured for frontend-backend communication
- Uses environment variables for FRONTEND_URL and RENDER_EXTERNAL_URL

## Common Commands
- Backend: `poetry install && poetry shell`
- Frontend: `cd frontend && npm install && npm start`
- API server: `python api.py` or `uvicorn api:app --reload`

## Recent Changes
- Latest commit: c7881d1 - CORS and API URL config for Render deployment
- Removed project_notes.md file
- Configured for production deployment on Render
- Fixed react-scripts version in package.json (changed from ^0.0.0 to 5.0.1)
- Frontend has 9 npm vulnerabilities (safe to ignore - all in dev dependencies: nth-check, postcss, webpack-dev-server)

## Development Notes
- Uses loguru for logging
- Pandas for data manipulation
- mplfinance for potential charting (backend)
- recharts for frontend charting
- Proper error handling in API endpoints