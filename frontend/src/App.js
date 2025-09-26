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
const API_SCAN_URL = 'http://127.0.0.1:8000/api/scan';
const API_HISTORY_URL = 'http://127.0.0.1:8000/api/history';

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

  // --- Handlers ---
  const handleAnalysisClick = async () => {
    setLoading(true);
    setError('');
    setResults([]);
    setSelectedStock(null);
    setChartData([]);

    const tickerList = tickers.split(',').map(t => t.trim()).filter(t => t);
    if (tickerList.length === 0) {
      setError('Please enter at least one ticker symbol.');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post(API_SCAN_URL, { tickers: tickerList });
      setResults(response.data);
    } catch (err) {
      setError('Failed to fetch data from the API. Please ensure the backend server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
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
      </Container>
    </Fragment>
  );
}

export default App;
