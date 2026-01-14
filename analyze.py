#!/usr/bin/env python3
"""
Trend Analysis Module
=====================

Performs local, offline analysis of collected Reddit data.
All processing happens on local machine - no external API calls.

COMPLIANCE NOTICE:
- This module processes ONLY locally stored, anonymized data
- No Reddit API calls are made from this module
- No personal user data is analyzed or stored
- Results are aggregated statistics only

Author: dreday2050
License: MIT
"""

import logging
from collections import Counter
from typing import List, Dict, Any

# Optional: Sentiment analysis (install with: pip install textblob)
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ============================================================================
# TEXT ANALYSIS FUNCTIONS (LOCAL PROCESSING ONLY)
# ============================================================================


def analyze_sentiment(text: str) -> Dict[str, float]:
    """
    Perform basic sentiment analysis on text.

    Uses TextBlob for simple polarity/subjectivity scoring.
    All processing is done locally - no external API calls.

    Args:
        text: Input text to analyze

    Returns:
        dict: Sentiment scores (polarity: -1 to 1, subjectivity: 0 to 1)
    """
    if not TEXTBLOB_AVAILABLE:
        logger.warning("TextBlob not installed. Skipping sentiment analysis.")
        return {"polarity": 0.0, "subjectivity": 0.0}

    blob = TextBlob(text)
    return {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity,
    }


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """
    Extract most common meaningful words from text.

    Simple keyword extraction using word frequency.
    Filters out common stop words.

    Args:
        text: Input text
        top_n: Number of top keywords to return

    Returns:
        list: Most frequent meaningful words
    """
    # Basic stop words to filter out
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "must", "shall", "can", "this",
        "that", "these", "those", "i", "you", "he", "she", "it", "we", "they",
        "what", "which", "who", "when", "where", "why", "how", "all", "each",
        "every", "both", "few", "more", "most", "other", "some", "such", "no",
        "not", "only", "same", "so", "than", "too", "very", "just", "also",
    }

    # Tokenize and filter
    words = text.lower().split()
    words = [w.strip(".,!?\"'()[]{}") for w in words]
    words = [w for w in words if w and len(w) > 2 and w not in stop_words]

    # Count and return top N
    word_counts = Counter(words)
    return [word for word, count in word_counts.most_common(top_n)]


def calculate_trend_metrics(posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate aggregate trend metrics from post data.

    PRIVACY NOTE: All metrics are aggregated - no individual user data.

    Args:
        posts: List of post data dictionaries

    Returns:
        dict: Aggregated metrics (averages, totals, trends)
    """
    if not posts:
        return {"error": "No posts to analyze"}

    total_posts = len(posts)
    total_score = sum(p.get("score", 0) for p in posts)
    total_comments = sum(p.get("num_comments", 0) for p in posts)

    return {
        "total_posts": total_posts,
        "average_score": total_score / total_posts,
        "average_comments": total_comments / total_posts,
        "total_engagement": total_score + total_comments,
    }


# ============================================================================
# MAIN (for standalone testing)
# ============================================================================


def main():
    """Demo function showing analysis capabilities."""
    logger.info("Trend Analysis Module - Demo")
    logger.info("This module performs LOCAL analysis only.")
    logger.info("No Reddit API calls are made from here.")

    # Example: Analyze sample text
    sample_text = "This is a sample post about peptide research and trends."

    sentiment = analyze_sentiment(sample_text)
    logger.info(f"Sample sentiment: {sentiment}")

    keywords = extract_keywords(sample_text)
    logger.info(f"Sample keywords: {keywords}")


if __name__ == "__main__":
    main()
