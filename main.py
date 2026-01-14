#!/usr/bin/env python3
"""
Reddit Peptide Discussion Trend Analyzer
=========================================

A read-only tool for analyzing public discussion trends in peptide-related
subreddits using the official Reddit API via PRAW.

COMPLIANCE NOTICE:
- This script performs READ-ONLY operations only
- No posting, voting, commenting, or any write operations
- Respects Reddit's rate limits (1-2 second delays between requests)
- Uses proper User-Agent identification
- For personal, non-commercial research only

Author: dreday2050
License: MIT
"""

import time
import logging
from datetime import datetime
from typing import Generator, Optional

import praw
from praw.models import Submission, Comment

# ============================================================================
# CONFIGURATION - Import from config.py (see config.example.py for template)
# ============================================================================

try:
    from config import (
        REDDIT_CLIENT_ID,
        REDDIT_CLIENT_SECRET,
        REDDIT_USER_AGENT,
    )
except ImportError:
    print("ERROR: config.py not found. Copy config.example.py to config.py")
    print("       and fill in your Reddit API credentials.")
    exit(1)

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTS
# ============================================================================

# Target subreddits for peptide discussion analysis
TARGET_SUBREDDITS = [
    "Peptides",
    # Add other relevant subreddits as needed
]

# Rate limiting: Minimum seconds between API requests
# Reddit allows ~60 requests/minute; we're conservative at ~30/minute
REQUEST_DELAY_SECONDS = 2.0

# Maximum items to fetch per request (Reddit's max is typically 100)
DEFAULT_FETCH_LIMIT = 25

# ============================================================================
# REDDIT CLIENT INITIALIZATION
# ============================================================================


def create_reddit_client() -> praw.Reddit:
    """
    Initialize and return a read-only Reddit client.

    The client is configured with:
    - Proper OAuth2 authentication
    - Descriptive User-Agent (required by Reddit)
    - Read-only mode (no write operations possible)

    Returns:
        praw.Reddit: Authenticated Reddit client instance
    """
    logger.info("Initializing Reddit client (read-only mode)...")

    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        # NOTE: No username/password = script runs in read-only mode
        # This is intentional - we only need to read public data
    )

    # Verify read-only status
    logger.info(f"Client initialized. Read-only mode: {reddit.read_only}")

    return reddit


# ============================================================================
# DATA FETCHING FUNCTIONS (READ-ONLY)
# ============================================================================


def fetch_subreddit_posts(
    reddit: praw.Reddit,
    subreddit_name: str,
    sort: str = "new",
    limit: int = DEFAULT_FETCH_LIMIT,
) -> Generator[Submission, None, None]:
    """
    Fetch posts from a subreddit using the specified sort method.

    This is a READ-ONLY operation that retrieves publicly available posts.
    Rate limiting is enforced between requests.

    Args:
        reddit: Authenticated Reddit client
        subreddit_name: Name of the subreddit (without r/)
        sort: Sort method - 'new', 'hot', 'top', 'rising'
        limit: Maximum number of posts to fetch

    Yields:
        Submission: Individual post objects

    Note:
        - Only public data is accessed
        - No user-specific or private data is collected
        - Rate limits are respected with built-in delays
    """
    logger.info(f"Fetching {limit} '{sort}' posts from r/{subreddit_name}...")

    subreddit = reddit.subreddit(subreddit_name)

    # Select the appropriate listing based on sort method
    if sort == "new":
        posts = subreddit.new(limit=limit)
    elif sort == "hot":
        posts = subreddit.hot(limit=limit)
    elif sort == "top":
        posts = subreddit.top(limit=limit, time_filter="week")
    elif sort == "rising":
        posts = subreddit.rising(limit=limit)
    else:
        logger.warning(f"Unknown sort '{sort}', defaulting to 'new'")
        posts = subreddit.new(limit=limit)

    for post in posts:
        yield post
        # RATE LIMITING: Wait between requests to respect Reddit's limits
        time.sleep(REQUEST_DELAY_SECONDS)


def extract_post_data(post: Submission) -> dict:
    """
    Extract relevant public data from a post for analysis.

    PRIVACY NOTE: Only public, non-identifying information is extracted.
    User-specific data (like usernames) is NOT stored for analysis.

    Args:
        post: A Reddit Submission object

    Returns:
        dict: Anonymized post data for trend analysis
    """
    return {
        "id": post.id,
        "created_utc": datetime.utcfromtimestamp(post.created_utc).isoformat(),
        "title": post.title,
        "selftext": post.selftext[:500] if post.selftext else "",  # Truncate for efficiency
        "score": post.score,
        "num_comments": post.num_comments,
        "upvote_ratio": post.upvote_ratio,
        "subreddit": str(post.subreddit),
        # NOTE: We do NOT store author/username information
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def main():
    """
    Main execution function.

    Demonstrates read-only data fetching from target subreddits.
    All operations are logged for transparency.
    """
    logger.info("=" * 60)
    logger.info("Reddit Peptide Trend Analyzer - Starting")
    logger.info("Mode: READ-ONLY | Commercial Use: NO")
    logger.info("=" * 60)

    # Initialize client
    reddit = create_reddit_client()

    # Verify we're in read-only mode
    if not reddit.read_only:
        logger.error("Client is not in read-only mode. Exiting for safety.")
        return

    # Fetch and display sample data
    for subreddit_name in TARGET_SUBREDDITS:
        logger.info(f"\n--- Processing r/{subreddit_name} ---")

        posts_processed = 0
        for post in fetch_subreddit_posts(reddit, subreddit_name, limit=10):
            post_data = extract_post_data(post)

            # Log basic info (anonymized)
            logger.info(
                f"Post: {post_data['title'][:50]}... | "
                f"Score: {post_data['score']} | "
                f"Comments: {post_data['num_comments']}"
            )

            posts_processed += 1

        logger.info(f"Processed {posts_processed} posts from r/{subreddit_name}")

    logger.info("\n" + "=" * 60)
    logger.info("Execution complete. No write operations performed.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
