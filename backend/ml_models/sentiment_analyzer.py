"""
Sentiment Analyzer Module
Uses FinBERT model for financial sentiment analysis
"""
from typing import List, Dict, Optional
from loguru import logger
import numpy as np


class SentimentAnalyzer:
    """Analyzes sentiment of financial news using FinBERT"""

    def __init__(self, model_name: str = "ProsusAI/finbert"):
        """
        Initialize sentiment analyzer with FinBERT model

        Args:
            model_name: Hugging Face model name (default: ProsusAI/finbert)
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self._load_model()

    def _load_model(self):
        """Load FinBERT model and tokenizer"""
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            import torch

            logger.info(f"Loading sentiment model: {self.model_name}")

            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

            # Set to evaluation mode
            self.model.eval()

            logger.info("Sentiment model loaded successfully")

        except Exception as e:
            logger.error(f"Error loading sentiment model: {e}")
            logger.warning("Sentiment analysis will use rule-based fallback")
            self.model = None
            self.tokenizer = None

    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text

        Args:
            text: Text to analyze

        Returns:
            Dict with sentiment label, score, and confidence
        """
        if not text or not text.strip():
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "confidence": 0.0,
                "positive": 0.33,
                "neutral": 0.34,
                "negative": 0.33
            }

        # Use FinBERT if available, otherwise fallback to rule-based
        if self.model and self.tokenizer:
            return self._analyze_with_finbert(text)
        else:
            return self._analyze_rule_based(text)

    def _analyze_with_finbert(self, text: str) -> Dict:
        """Analyze sentiment using FinBERT model"""
        try:
            import torch

            # Tokenize and prepare input
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )

            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # FinBERT outputs: [positive, negative, neutral]
            scores = predictions[0].tolist()

            # Map to labels
            labels = ["positive", "negative", "neutral"]
            sentiment_scores = {labels[i]: scores[i] for i in range(len(labels))}

            # Determine dominant sentiment
            max_label = labels[np.argmax(scores)]
            max_score = max(scores)

            # Convert to -1 to +1 scale
            # positive: +1, negative: -1, neutral: 0
            normalized_score = (
                sentiment_scores["positive"] - sentiment_scores["negative"]
            )

            return {
                "sentiment": max_label,
                "score": normalized_score,  # -1 (very negative) to +1 (very positive)
                "confidence": max_score,
                "positive": sentiment_scores["positive"],
                "neutral": sentiment_scores["neutral"],
                "negative": sentiment_scores["negative"]
            }

        except Exception as e:
            logger.error(f"Error in FinBERT analysis: {e}")
            return self._analyze_rule_based(text)

    def _analyze_rule_based(self, text: str) -> Dict:
        """
        Simple rule-based sentiment analysis (fallback)
        Used when FinBERT is not available
        """
        text_lower = text.lower()

        # Positive keywords
        positive_words = [
            "growth", "profit", "gain", "surge", "beat", "strong", "upgrade",
            "bullish", "positive", "increase", "rally", "outperform", "success",
            "excellent", "record", "breakthrough", "innovation", "expansion"
        ]

        # Negative keywords
        negative_words = [
            "loss", "decline", "fall", "drop", "weak", "downgrade", "bearish",
            "negative", "decrease", "plunge", "underperform", "fail", "concern",
            "risk", "warning", "cut", "layoff", "recession"
        ]

        # Count positive and negative words
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        total = positive_count + negative_count

        if total == 0:
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "confidence": 0.5,
                "positive": 0.33,
                "neutral": 0.34,
                "negative": 0.33
            }

        # Calculate scores
        pos_ratio = positive_count / total if total > 0 else 0.33
        neg_ratio = negative_count / total if total > 0 else 0.33
        neu_ratio = 1 - (pos_ratio + neg_ratio)

        # Normalize to -1 to +1
        score = (positive_count - negative_count) / max(total, 1)

        # Determine sentiment
        if score > 0.2:
            sentiment = "positive"
        elif score < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "score": score,
            "confidence": max(pos_ratio, neg_ratio, neu_ratio),
            "positive": pos_ratio,
            "neutral": neu_ratio,
            "negative": neg_ratio
        }

    def analyze_articles(self, articles: List[Dict]) -> Dict:
        """
        Analyze sentiment of multiple news articles

        Args:
            articles: List of article dictionaries with 'title' and 'description'

        Returns:
            Aggregated sentiment analysis with individual article scores
        """
        if not articles:
            return {
                "overall_sentiment": "neutral",
                "overall_score": 0.0,
                "confidence": 0.0,
                "article_count": 0,
                "articles": []
            }

        article_sentiments = []

        for article in articles:
            # Combine title and description for analysis
            title = article.get("title", "")
            description = article.get("description", "")
            text = f"{title}. {description}"

            sentiment = self.analyze_text(text)

            article_sentiments.append({
                "title": title,
                "sentiment": sentiment["sentiment"],
                "score": sentiment["score"],
                "confidence": sentiment["confidence"],
                "published_at": article.get("published_at", ""),
                "source": article.get("source", "")
            })

        # Calculate overall sentiment with time decay
        overall_score = self._calculate_weighted_sentiment(article_sentiments)

        # Determine overall sentiment label
        if overall_score > 0.15:
            overall_sentiment = "positive"
        elif overall_score < -0.15:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"

        # Calculate average confidence
        avg_confidence = np.mean([a["confidence"] for a in article_sentiments])

        return {
            "overall_sentiment": overall_sentiment,
            "overall_score": overall_score,
            "confidence": float(avg_confidence),
            "article_count": len(articles),
            "positive_count": sum(1 for a in article_sentiments if a["sentiment"] == "positive"),
            "negative_count": sum(1 for a in article_sentiments if a["sentiment"] == "negative"),
            "neutral_count": sum(1 for a in article_sentiments if a["sentiment"] == "neutral"),
            "articles": article_sentiments
        }

    def _calculate_weighted_sentiment(self, article_sentiments: List[Dict]) -> float:
        """
        Calculate weighted sentiment score with time decay
        Recent articles have more weight
        """
        if not article_sentiments:
            return 0.0

        # Simple average for now - can add time decay later
        scores = [a["score"] for a in article_sentiments]
        return float(np.mean(scores))


# Singleton instance for reuse
_sentiment_analyzer_instance: Optional[SentimentAnalyzer] = None


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """
    Get or create sentiment analyzer singleton instance

    Returns:
        SentimentAnalyzer instance
    """
    global _sentiment_analyzer_instance

    if _sentiment_analyzer_instance is None:
        _sentiment_analyzer_instance = SentimentAnalyzer()

    return _sentiment_analyzer_instance
