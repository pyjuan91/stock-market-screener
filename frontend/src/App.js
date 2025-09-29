import React, { useState, useEffect, Fragment } from 'react';
import axios from 'axios';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  CssBaseline,
  TextField,
  Button,
  Box,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

// Define the backend API URLs
// Use environment variable for production, fallback to localhost for development
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
const API_SCAN_URL = `${API_BASE_URL}/api/scan`;
const API_HISTORY_URL = `${API_BASE_URL}/api/history`;

console.log('API_BASE_URL:', API_BASE_URL); // Debug log for deployment

// --- Cache Data for Demo ---
const CACHE_DATA = {
  'AAPL': { ticker: 'AAPL', Close: 178.42, RSI: 65.32, MACD: 1.23, MACD_Signal: 1.15, MA20: 175.67, MA50: 172.34 },
  'GOOG': { ticker: 'GOOG', Close: 2742.19, RSI: 58.47, MACD: 15.67, MACD_Signal: 14.23, MA20: 2735.89, MA50: 2720.45 },
  'GOOGL': { ticker: 'GOOGL', Close: 2742.19, RSI: 58.47, MACD: 15.67, MACD_Signal: 14.23, MA20: 2735.89, MA50: 2720.45 },
  'MSFT': { ticker: 'MSFT', Close: 412.83, RSI: 62.15, MACD: 3.45, MACD_Signal: 3.12, MA20: 410.56, MA50: 405.78 },
  'AMZN': { ticker: 'AMZN', Close: 3312.68, RSI: 55.89, MACD: 25.34, MACD_Signal: 23.67, MA20: 3305.21, MA50: 3290.87 },
  'TSLA': { ticker: 'TSLA', Close: 248.50, RSI: 71.23, MACD: 8.76, MACD_Signal: 7.89, MA20: 245.67, MA50: 238.92 },
  'META': { ticker: 'META', Close: 484.52, RSI: 59.67, MACD: 12.45, MACD_Signal: 11.78, MA20: 481.34, MA50: 475.23 },
  'NVDA': { ticker: 'NVDA', Close: 875.28, RSI: 68.94, MACD: 18.92, MACD_Signal: 17.56, MA20: 870.45, MA50: 860.12 },
  'NFLX': { ticker: 'NFLX', Close: 486.81, RSI: 52.36, MACD: 6.78, MACD_Signal: 6.45, MA20: 485.67, MA50: 482.34 },
  'CRM': { ticker: 'CRM', Close: 284.76, RSI: 61.23, MACD: 4.56, MACD_Signal: 4.12, MA20: 282.89, MA50: 278.45 }
};

// --- Helper Functions for Chart Formatting ---
const currencyFormatter = (value) => `${value.toFixed(2)}`;
const decimalFormatter = (value) => value.toFixed(2);

// --- Main App Component ---
function App() {
  // State for the main ticker input and analysis results
  const [tickers, setTickers] = useState('AAPL, GOOG, MSFT');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // State for the detailed view (charts)
  const [selectedStock, setSelectedStock] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [chartLoading, setChartLoading] = useState(false);
  const [chartError, setChartError] = useState('');

  // State for timeout dialog
  const [showTimeoutDialog, setShowTimeoutDialog] = useState(false);
  const [pendingTickers, setPendingTickers] = useState([]);

  // --- Handlers ---
  const handleAnalysisClick = async () => {
    setLoading(true);
    setError('');
    setResults([]);
    setSelectedStock(null);
    setChartData([]);

    const tickerList = tickers.split(',').map(t => t.trim().toUpperCase()).filter(t => t);
    if (tickerList.length === 0) {
      setError('Please enter at least one ticker symbol.');
      setLoading(false);
      return;
    }

    try {
      // Create a timeout promise
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('timeout')), 3000)
      );

      // Race between API call and timeout
      const apiPromise = axios.post(API_SCAN_URL, { tickers: tickerList });
      const response = await Promise.race([apiPromise, timeoutPromise]);

      setResults(response.data);
    } catch (err) {
      if (err.message === 'timeout') {
        // Backend is likely sleeping on Render.com
        setPendingTickers(tickerList);
        setShowTimeoutDialog(true);
      } else {
        setError('Failed to fetch data from the API. Please ensure the backend server is running.');
        console.error(err);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleUseCacheData = () => {
    const cacheResults = pendingTickers
      .filter(ticker => CACHE_DATA[ticker])
      .map(ticker => CACHE_DATA[ticker]);

    setResults(cacheResults);
    setShowTimeoutDialog(false);
    setPendingTickers([]);
  };

  const handleWaitForBackend = () => {
    setShowTimeoutDialog(false);
    setPendingTickers([]);
    // Retry the analysis
    handleAnalysisClick();
  };

  const handleCancelAnalysis = () => {
    setShowTimeoutDialog(false);
    setPendingTickers([]);
  };

  const handleRowClick = (row) => {
    if (selectedStock?.ticker === row.ticker) {
      setSelectedStock(null);
      setChartData([]);
    } else {
      setSelectedStock(row);
    }
  };

  // --- Effects ---
  useEffect(() => {
    if (!selectedStock) return;

    const fetchChartData = async () => {
      setChartLoading(true);
      setChartError('');
      setChartData([]);

      try {
        const response = await axios.get(`${API_HISTORY_URL}/${selectedStock.ticker}`);
        setChartData(response.data);
      } catch (err) {
        setChartError(`Failed to fetch historical data for ${selectedStock.ticker}.`);
        console.error(err);
      } finally {
        setChartLoading(false);
      }
    };

    fetchChartData();
  }, [selectedStock]);

  // --- Render ---
  const chartMargin = { top: 20, right: 30, left: 30, bottom: 10 };

  return (
    <Fragment>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div">Stock Market Screener</Typography>
        </Toolbar>
      </AppBar>

      <Container style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
        {/* Input Section */}
        <Typography variant="h4" gutterBottom>Enter Stock Tickers</Typography>
        <Typography variant="body1" color="textSecondary" gutterBottom>Enter one or more ticker symbols, separated by commas.</Typography>
        <Box display="flex" alignItems="center" marginTop="1.5rem">
          <TextField
            fullWidth
            variant="outlined"
            label="Tickers (e.g., AAPL, GOOG, MSFT)"
            value={tickers}
            onChange={(e) => setTickers(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !loading) {
                handleAnalysisClick();
              }
            }}
            disabled={loading}
          />
          <Button variant="contained" color="primary" onClick={handleAnalysisClick} disabled={loading} style={{ marginLeft: '1rem', height: '56px', width: '120px' }}>
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Analyze'}
          </Button>
        </Box>

        {error && <Typography color="error" style={{ marginTop: '1rem' }}>{error}</Typography>}

        {/* Results Table */}
        {results.length > 0 && (
          <Box marginTop="2rem">
            <Typography variant="h5" gutterBottom>Analysis Results</Typography>
            <Typography variant="body2" color="textSecondary" gutterBottom>Click on a row to view historical charts.</Typography>
            <TableContainer component={Paper} style={{ marginTop: '1rem' }}>
              <Table sx={{ minWidth: 650 }} aria-label="analysis results table">
                <TableHead>
                  <TableRow>
                    <TableCell>Ticker</TableCell>
                    <TableCell align="right">Close</TableCell>
                    <TableCell align="right">RSI</TableCell>
                    <TableCell align="right">MACD</TableCell>
                    <TableCell align="right">MACD Signal</TableCell>
                    <TableCell align="right">MA20</TableCell>
                    <TableCell align="right">MA50</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {results.map((row) => (
                    <TableRow key={row.ticker} hover onClick={() => handleRowClick(row)} selected={selectedStock?.ticker === row.ticker} style={{ cursor: 'pointer' }} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                      <TableCell component="th" scope="row">{row.ticker}</TableCell>
                      <TableCell align="right">{row.Close?.toFixed(2)}</TableCell>
                      <TableCell align="right">{row.RSI?.toFixed(2)}</TableCell>
                      <TableCell align="right">{row.MACD?.toFixed(2)}</TableCell>
                      <TableCell align="right">{row.MACD_Signal?.toFixed(2)}</TableCell>
                      <TableCell align="right">{row.MA20?.toFixed(2)}</TableCell>
                      <TableCell align="right">{row.MA50?.toFixed(2)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}

        {/* Chart Section */}
        {selectedStock && (
          <Box marginTop="4rem">
            <Typography variant="h5" gutterBottom>Historical Charts for {selectedStock.ticker}</Typography>
            {chartLoading && <Box textAlign="center" padding="2rem"><CircularProgress /></Box>}
            {chartError && <Typography color="error">{chartError}</Typography>}
            {chartData.length > 0 && (
              <Fragment>
                <Typography variant="h6" style={{ marginTop: '2.5rem' }}>Price & Moving Averages</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={chartData} syncId="stock_charts" margin={chartMargin}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" interval={"preserveStartEnd"} />
                    <YAxis domain={['dataMin - dataMin * 0.05', 'dataMax + dataMax * 0.05']} tickFormatter={currencyFormatter} />
                    <Tooltip formatter={currencyFormatter} />
                    <Legend />
                    <Line type="monotone" dataKey="Close" stroke="#8884d8" name="Price" dot={false} />
                    <Line type="monotone" dataKey="MA20" stroke="#82ca9d" name="MA 20" dot={false} />
                    <Line type="monotone" dataKey="MA50" stroke="#ffc658" name="MA 50" dot={false} />
                  </LineChart>
                </ResponsiveContainer>

                <Typography variant="h6" style={{ marginTop: '2.5rem' }}>RSI (Relative Strength Index)</Typography>
                <ResponsiveContainer width="100%" height={150}>
                  <LineChart data={chartData} syncId="stock_charts" margin={chartMargin}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" interval={"preserveStartEnd"} />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="RSI" stroke="#8884d8" activeDot={{ r: 8 }} dot={false} />
                    <Line type="monotone" dataKey={() => 70} stroke="#ff0000" strokeDasharray="5 5" name="Overbought" dot={false} />
                    <Line type="monotone" dataKey={() => 30} stroke="#00ff00" strokeDasharray="5 5" name="Oversold" dot={false} />
                  </LineChart>
                </ResponsiveContainer>

                <Typography variant="h6" style={{ marginTop: '2.5rem' }}>MACD (Moving Average Convergence Divergence)</Typography>
                <ResponsiveContainer width="100%" height={150}>
                  <LineChart data={chartData} syncId="stock_charts" margin={chartMargin}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" interval={"preserveStartEnd"} />
                    <YAxis tickFormatter={decimalFormatter} />
                    <Tooltip formatter={decimalFormatter} />
                    <Legend />
                    <Line type="monotone" dataKey="MACD" stroke="#82ca9d" dot={false} />
                    <Line type="monotone" dataKey="MACD_Signal" stroke="#ffc658" name="Signal" dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </Fragment>
            )}
          </Box>
        )}

        {/* Timeout Dialog */}
        <Dialog open={showTimeoutDialog} onClose={handleCancelAnalysis}>
          <DialogTitle>Backend Server Sleeping</DialogTitle>
          <DialogContent>
            <DialogContentText>
              The backend server on Render.com appears to be sleeping and taking longer than expected to respond.
              This usually happens when the server hasn't been used for a while.
              <br /><br />
              You can either wait for the server to wake up (this may take 30-60 seconds), or use cached demo data for the following stocks:
              <br /><br />
              <strong>Available cached stocks:</strong> {pendingTickers.filter(ticker => CACHE_DATA[ticker]).join(', ')}
              {pendingTickers.some(ticker => !CACHE_DATA[ticker]) && (
                <>
                  <br />
                  <strong>Not available in cache:</strong> {pendingTickers.filter(ticker => !CACHE_DATA[ticker]).join(', ')}
                </>
              )}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCancelAnalysis} color="secondary">
              Cancel
            </Button>
            <Button onClick={handleWaitForBackend} color="primary">
              Wait for Server
            </Button>
            <Button
              onClick={handleUseCacheData}
              color="primary"
              variant="contained"
              disabled={!pendingTickers.some(ticker => CACHE_DATA[ticker])}
            >
              Use Cached Data
            </Button>
          </DialogActions>
        </Dialog>
      </Container>
    </Fragment>
  );
}

export default App;
