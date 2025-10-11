"""
News Fetcher Module
Fetches financial news from multiple sources for sentiment analysis
"""
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
import requests


class NewsFetcher:
    """Fetches news articles for stock symbols from various sources"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize news fetcher

        Args:
            api_key: NewsAPI key (defaults to environment variable NEWS_API_KEY)
        """
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.newsapi_base_url = "https://newsapi.org/v2/everything"

    def fetch_newsapi(self, ticker: str, days: int = 7, max_results: int = 20) -> List[Dict]:
        """
        Fetch news from NewsAPI

        Args:
            ticker: Stock ticker symbol
            days: Number of days to look back
            max_results: Maximum number of articles to return

        Returns:
            List of news articles with title, description, source, and published date
        """
        if not self.api_key:
            logger.warning("NEWS_API_KEY not set, using fallback demo data")
            return self._get_demo_news(ticker)

        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            params = {
                "q": f"{ticker} OR stock OR shares",
                "from": from_date,
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": max_results,
                "apiKey": self.api_key
            }

            response = requests.get(self.newsapi_base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("status") != "ok":
                logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                return self._get_demo_news(ticker)

            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "content": article.get("content", ""),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "published_at": article.get("publishedAt", ""),
                    "url": article.get("url", "")
                })

            logger.info(f"Fetched {len(articles)} news articles for {ticker}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {e}")
            return self._get_demo_news(ticker)

    def fetch_finnhub(self, ticker: str, days: int = 7) -> List[Dict]:
        """
        Fetch news from Finnhub (alternative free source)

        Args:
            ticker: Stock ticker symbol
            days: Number of days to look back

        Returns:
            List of news articles
        """
        # Implementation for Finnhub API
        # Requires FINNHUB_API_KEY environment variable
        finnhub_key = os.getenv("FINNHUB_API_KEY")

        if not finnhub_key:
            logger.warning("FINNHUB_API_KEY not set, skipping Finnhub news")
            return []

        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            to_date = datetime.now().strftime("%Y-%m-%d")

            url = f"https://finnhub.io/api/v1/company-news"
            params = {
                "symbol": ticker,
                "from": from_date,
                "to": to_date,
                "token": finnhub_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            articles = []
            for article in response.json():
                articles.append({
                    "title": article.get("headline", ""),
                    "description": article.get("summary", ""),
                    "content": article.get("summary", ""),
                    "source": article.get("source", "Finnhub"),
                    "published_at": datetime.fromtimestamp(article.get("datetime", 0)).isoformat(),
                    "url": article.get("url", "")
                })

            logger.info(f"Fetched {len(articles)} Finnhub articles for {ticker}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching Finnhub news for {ticker}: {e}")
            return []

    def fetch_all_sources(self, ticker: str, days: int = 7) -> List[Dict]:
        """
        Aggregate news from all available sources

        Args:
            ticker: Stock ticker symbol
            days: Number of days to look back

        Returns:
            Combined list of news articles from all sources
        """
        all_articles = []

        # Fetch from NewsAPI
        newsapi_articles = self.fetch_newsapi(ticker, days)
        all_articles.extend(newsapi_articles)

        # Fetch from Finnhub
        finnhub_articles = self.fetch_finnhub(ticker, days)
        all_articles.extend(finnhub_articles)

        # Remove duplicates based on title similarity
        unique_articles = self._remove_duplicates(all_articles)

        # Sort by published date (most recent first)
        unique_articles.sort(key=lambda x: x.get("published_at", ""), reverse=True)

        logger.info(f"Total {len(unique_articles)} unique articles for {ticker}")
        return unique_articles

    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique = []

        for article in articles:
            title = article.get("title", "").lower()
            # Simple duplicate detection - can be improved with fuzzy matching
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique.append(article)

        return unique

    def _get_demo_news(self, ticker: str) -> List[Dict]:
        """
        Return demo news data when API is not available
        Useful for development and demos
        """
        demo_data = {
            "AAPL": [
                {
                    "title": f"{ticker} Reports Strong Quarterly Earnings",
                    "description": f"{ticker} exceeded analyst expectations with robust revenue growth.",
                    "content": "Strong performance across all product lines...",
                    "source": "Demo Financial News",
                    "published_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                    "url": "https://example.com/demo"
                },
                {
                    "title": f"Analysts Upgrade {ticker} Price Target",
                    "description": "Major investment banks raise price targets following positive outlook.",
                    "content": "Increased consumer demand and innovation...",
                    "source": "Demo Market Watch",
                    "published_at": (datetime.now() - timedelta(hours=6)).isoformat(),
                    "url": "https://example.com/demo"
                },
                {
                    "title": f"{ticker} Announces New Product Line",
                    "description": "Company unveils innovative products at annual event.",
                    "content": "Significant technological advancements...",
                    "source": "Demo Tech News",
                    "published_at": (datetime.now() - timedelta(days=1)).isoformat(),
                    "url": "https://example.com/demo"
                }
            ],
            "TSLA": [
                {
                    "title": f"{ticker} Delivery Numbers Beat Expectations",
                    "description": "Electric vehicle deliveries surge in latest quarter.",
                    "content": "Record production and delivery numbers...",
                    "source": "Demo Auto News",
                    "published_at": (datetime.now() - timedelta(hours=3)).isoformat(),
                    "url": "https://example.com/demo"
                },
                {
                    "title": f"{ticker} Expands Manufacturing Capacity",
                    "description": "New factory to boost production capabilities.",
                    "content": "Strategic expansion in key markets...",
                    "source": "Demo Industry Report",
                    "published_at": (datetime.now() - timedelta(hours=8)).isoformat(),
                    "url": "https://example.com/demo"
                }
            ]
        }

        # Return demo data for ticker or generic positive news
        return demo_data.get(ticker, [
            {
                "title": f"{ticker} Stock Shows Positive Momentum",
                "description": f"Market analysts optimistic about {ticker} future prospects.",
                "content": "Strong fundamentals and market position...",
                "source": "Demo Financial Times",
                "published_at": (datetime.now() - timedelta(hours=4)).isoformat(),
                "url": "https://example.com/demo"
            },
            {
                "title": f"{ticker} Maintains Strong Market Position",
                "description": "Company continues to perform well in competitive landscape.",
                "content": "Consistent growth and innovation...",
                "source": "Demo Business Wire",
                "published_at": (datetime.now() - timedelta(hours=12)).isoformat(),
                "url": "https://example.com/demo"
            }
        ])
