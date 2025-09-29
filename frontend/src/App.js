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
  ThemeProvider,
  createTheme,
  Card,
  CardContent,
  Chip,
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

// --- Apple-style Theme ---
const appleTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#007AFF', // Apple blue
      light: '#4DA6FF',
      dark: '#0056CC',
    },
    secondary: {
      main: '#FF9500', // Apple orange
      light: '#FFB84D',
      dark: '#CC7700',
    },
    background: {
      default: '#F2F2F7', // Apple light gray background
      paper: '#FFFFFF',
    },
    text: {
      primary: '#1D1D1F', // Apple dark text
      secondary: '#86868B', // Apple gray text
    },
    error: {
      main: '#FF3B30', // Apple red
    },
    success: {
      main: '#34C759', // Apple green
    },
    divider: '#D1D1D6',
  },
  typography: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    h4: {
      fontWeight: 700,
      fontSize: '2.125rem',
      lineHeight: 1.2,
      letterSpacing: '-0.02em',
      color: '#1D1D1F',
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.5rem',
      lineHeight: 1.3,
      letterSpacing: '-0.01em',
      color: '#1D1D1F',
    },
    h6: {
      fontWeight: 600,
      fontSize: '1.25rem',
      lineHeight: 1.4,
      color: '#1D1D1F',
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5,
      color: '#1D1D1F',
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.43,
      color: '#86868B',
    },
  },
  shape: {
    borderRadius: 12, // Apple's rounded corners
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 8,
          padding: '10px 20px',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          },
        },
        contained: {
          background: 'linear-gradient(135deg, #007AFF 0%, #0056CC 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #0056CC 0%, #004499 100%)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
            backgroundColor: '#FFFFFF',
            '& fieldset': {
              borderColor: '#D1D1D6',
            },
            '&:hover fieldset': {
              borderColor: '#007AFF',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#007AFF',
              borderWidth: 2,
            },
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 16px rgba(0, 0, 0, 0.08)',
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        head: {
          backgroundColor: '#F2F2F7',
          fontWeight: 600,
          color: '#1D1D1F',
          borderBottom: '1px solid #D1D1D6',
        },
        body: {
          borderBottom: '1px solid #F2F2F7',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#FFFFFF',
          color: '#1D1D1F',
          boxShadow: '0 1px 0 rgba(0, 0, 0, 0.1)',
        },
      },
    },
  },
});

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
    <ThemeProvider theme={appleTheme}>
      <CssBaseline />
      <AppBar position="static" elevation={0}>
        <Toolbar sx={{ minHeight: '80px !important' }}>
          <Typography variant="h6" component="div" sx={{ fontWeight: 700, fontSize: '1.375rem' }}>
            Stock Market Screener
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 6, pb: 8 }}>
        {/* Input Section */}
        <Card sx={{ mb: 4, p: 4 }}>
          <CardContent sx={{ p: 0, '&:last-child': { pb: 0 } }}>
            <Typography variant="h4" gutterBottom sx={{ mb: 1 }}>
              Enter Stock Tickers
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
              Enter one or more ticker symbols, separated by commas.
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder="AAPL, GOOG, MSFT"
                value={tickers}
                onChange={(e) => setTickers(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !loading) {
                    handleAnalysisClick();
                  }
                }}
                disabled={loading}
                sx={{ flex: 1 }}
              />
              <Button
                variant="contained"
                color="primary"
                onClick={handleAnalysisClick}
                disabled={loading}
                sx={{
                  minWidth: 120,
                  height: 56,
                  fontSize: '1rem',
                  fontWeight: 600
                }}
              >
                {loading ? <CircularProgress size={24} color="inherit" /> : 'Analyze'}
              </Button>
            </Box>
          </CardContent>
        </Card>

        {error && (
          <Card sx={{ mb: 4, bgcolor: 'error.main', color: 'white' }}>
            <CardContent>
              <Typography variant="body1">{error}</Typography>
            </CardContent>
          </Card>
        )}

        {/* Results Table */}
        {results.length > 0 && (
          <Card sx={{ mb: 4 }}>
            <CardContent sx={{ p: 4 }}>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h5" gutterBottom sx={{ mb: 1 }}>
                  Analysis Results
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Click on a row to view historical charts.
                </Typography>
              </Box>
              <TableContainer>
                <Table sx={{ minWidth: 650 }} aria-label="analysis results table">
                  <TableHead>
                    <TableRow>
                      <TableCell sx={{ fontWeight: 600, fontSize: '0.875rem' }}>Ticker</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.875rem' }}>Close</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.875rem' }}>RSI</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.875rem' }}>MACD</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.875rem' }}>MACD Signal</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.875rem' }}>MA20</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 600, fontSize: '0.875rem' }}>MA50</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {results.map((row) => (
                      <TableRow
                        key={row.ticker}
                        hover
                        onClick={() => handleRowClick(row)}
                        selected={selectedStock?.ticker === row.ticker}
                        sx={{
                          cursor: 'pointer',
                          '&:hover': {
                            backgroundColor: '#F2F2F7',
                          },
                          '&.Mui-selected': {
                            backgroundColor: '#E3F2FD',
                            '&:hover': {
                              backgroundColor: '#BBDEFB',
                            },
                          },
                        }}
                      >
                        <TableCell component="th" scope="row">
                          <Chip
                            label={row.ticker}
                            size="small"
                            sx={{
                              fontWeight: 600,
                              bgcolor: selectedStock?.ticker === row.ticker ? 'primary.main' : 'grey.100',
                              color: selectedStock?.ticker === row.ticker ? 'white' : 'text.primary',
                            }}
                          />
                        </TableCell>
                        <TableCell align="right" sx={{ fontWeight: 500 }}>${row.Close?.toFixed(2)}</TableCell>
                        <TableCell align="right">{row.RSI?.toFixed(2)}</TableCell>
                        <TableCell align="right">{row.MACD?.toFixed(2)}</TableCell>
                        <TableCell align="right">{row.MACD_Signal?.toFixed(2)}</TableCell>
                        <TableCell align="right">${row.MA20?.toFixed(2)}</TableCell>
                        <TableCell align="right">${row.MA50?.toFixed(2)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        )}

        {/* Chart Section */}
        {selectedStock && (
          <Card sx={{ mb: 4 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h5" gutterBottom sx={{ mb: 1 }}>
                Historical Charts for {selectedStock.ticker}
              </Typography>
              {chartLoading && (
                <Box textAlign="center" py={6}>
                  <CircularProgress size={40} />
                </Box>
              )}
              {chartError && (
                <Card sx={{ bgcolor: 'error.main', color: 'white', mb: 2 }}>
                  <CardContent>
                    <Typography variant="body1">{chartError}</Typography>
                  </CardContent>
                </Card>
              )}
              {chartData.length > 0 && (
                <Box>
                  <Box sx={{ mt: 4 }}>
                    <Typography variant="h6" gutterBottom sx={{ mb: 2, color: 'text.primary' }}>
                      Price & Moving Averages
                    </Typography>
                    <Box sx={{ bgcolor: '#FAFAFA', borderRadius: 2, p: 2 }}>
                      <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={chartData} syncId="stock_charts" margin={chartMargin}>
                          <CartesianGrid strokeDasharray="2 2" stroke="#E0E0E0" />
                          <XAxis dataKey="time" interval={"preserveStartEnd"} tick={{ fontSize: 12 }} />
                          <YAxis domain={['dataMin - dataMin * 0.05', 'dataMax + dataMax * 0.05']} tickFormatter={currencyFormatter} tick={{ fontSize: 12 }} />
                          <Tooltip formatter={currencyFormatter} contentStyle={{ backgroundColor: '#FFFFFF', border: '1px solid #D1D1D6', borderRadius: 8 }} />
                          <Legend />
                          <Line type="monotone" dataKey="Close" stroke="#007AFF" name="Price" dot={false} strokeWidth={2} />
                          <Line type="monotone" dataKey="MA20" stroke="#34C759" name="MA 20" dot={false} strokeWidth={2} />
                          <Line type="monotone" dataKey="MA50" stroke="#FF9500" name="MA 50" dot={false} strokeWidth={2} />
                        </LineChart>
                      </ResponsiveContainer>
                    </Box>
                  </Box>

                  <Box sx={{ mt: 4 }}>
                    <Typography variant="h6" gutterBottom sx={{ mb: 2, color: 'text.primary' }}>
                      RSI (Relative Strength Index)
                    </Typography>
                    <Box sx={{ bgcolor: '#FAFAFA', borderRadius: 2, p: 2 }}>
                      <ResponsiveContainer width="100%" height={150}>
                        <LineChart data={chartData} syncId="stock_charts" margin={chartMargin}>
                          <CartesianGrid strokeDasharray="2 2" stroke="#E0E0E0" />
                          <XAxis dataKey="time" interval={"preserveStartEnd"} tick={{ fontSize: 12 }} />
                          <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
                          <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', border: '1px solid #D1D1D6', borderRadius: 8 }} />
                          <Legend />
                          <Line type="monotone" dataKey="RSI" stroke="#007AFF" activeDot={{ r: 6 }} dot={false} strokeWidth={2} />
                          <Line type="monotone" dataKey={() => 70} stroke="#FF3B30" strokeDasharray="5 5" name="Overbought" dot={false} strokeWidth={1} />
                          <Line type="monotone" dataKey={() => 30} stroke="#34C759" strokeDasharray="5 5" name="Oversold" dot={false} strokeWidth={1} />
                        </LineChart>
                      </ResponsiveContainer>
                    </Box>
                  </Box>

                  <Box sx={{ mt: 4 }}>
                    <Typography variant="h6" gutterBottom sx={{ mb: 2, color: 'text.primary' }}>
                      MACD (Moving Average Convergence Divergence)
                    </Typography>
                    <Box sx={{ bgcolor: '#FAFAFA', borderRadius: 2, p: 2 }}>
                      <ResponsiveContainer width="100%" height={150}>
                        <LineChart data={chartData} syncId="stock_charts" margin={chartMargin}>
                          <CartesianGrid strokeDasharray="2 2" stroke="#E0E0E0" />
                          <XAxis dataKey="time" interval={"preserveStartEnd"} tick={{ fontSize: 12 }} />
                          <YAxis tickFormatter={decimalFormatter} tick={{ fontSize: 12 }} />
                          <Tooltip formatter={decimalFormatter} contentStyle={{ backgroundColor: '#FFFFFF', border: '1px solid #D1D1D6', borderRadius: 8 }} />
                          <Legend />
                          <Line type="monotone" dataKey="MACD" stroke="#34C759" dot={false} strokeWidth={2} />
                          <Line type="monotone" dataKey="MACD_Signal" stroke="#FF9500" name="Signal" dot={false} strokeWidth={2} />
                        </LineChart>
                      </ResponsiveContainer>
                    </Box>
                  </Box>
                </Box>
              )}
            </CardContent>
          </Card>
        )}

        {/* Timeout Dialog */}
        <Dialog
          open={showTimeoutDialog}
          onClose={handleCancelAnalysis}
          PaperProps={{
            sx: {
              borderRadius: 3,
              minWidth: 400,
            },
          }}
        >
          <DialogTitle sx={{ pb: 1, fontWeight: 600 }}>
            Backend Server Sleeping
          </DialogTitle>
          <DialogContent>
            <DialogContentText sx={{ mb: 2 }}>
              The backend server on Render.com appears to be sleeping and taking longer than expected to respond.
              This usually happens when the server hasn't been used for a while.
            </DialogContentText>
            <DialogContentText sx={{ mb: 2 }}>
              You can either wait for the server to wake up (this may take 30-60 seconds), or use cached demo data for the following stocks:
            </DialogContentText>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                Available cached stocks:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                {pendingTickers.filter(ticker => CACHE_DATA[ticker]).map(ticker => (
                  <Chip key={ticker} label={ticker} size="small" color="primary" />
                ))}
              </Box>
              {pendingTickers.some(ticker => !CACHE_DATA[ticker]) && (
                <>
                  <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                    Not available in cache:
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    {pendingTickers.filter(ticker => !CACHE_DATA[ticker]).map(ticker => (
                      <Chip key={ticker} label={ticker} size="small" color="default" />
                    ))}
                  </Box>
                </>
              )}
            </Box>
          </DialogContent>
          <DialogActions sx={{ px: 3, pb: 3 }}>
            <Button onClick={handleCancelAnalysis} color="secondary" sx={{ mr: 1 }}>
              Cancel
            </Button>
            <Button onClick={handleWaitForBackend} color="primary" sx={{ mr: 1 }}>
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
    </ThemeProvider>
  );
}

export default App;
