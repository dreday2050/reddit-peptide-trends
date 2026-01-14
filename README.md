# Reddit Peptide Discussion Trend Analyzer

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Reddit API](https://img.shields.io/badge/Reddit-API%20Compliant-FF4500.svg)](https://www.reddit.com/wiki/api)
[![Read-Only](https://img.shields.io/badge/Mode-Read--Only-brightgreen.svg)](#compliance)

A **personal, non-commercial** Python tool for read-only analysis of public discussion trends in peptide-related subreddits. Built with full compliance to Reddit's [API Terms of Use](https://www.redditinc.com/policies/data-api-terms) and [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki).

---

## Overview

This project fetches publicly available posts and comments from peptide-focused subreddits using [PRAW](https://praw.readthedocs.io/) (Python Reddit API Wrapper) to analyze discussion trends, sentiment patterns, and topic frequency over time.

### Key Features

- **100% Read-Only**: No posting, voting, commenting, or any write operations
- **Rate-Limited**: Respects Reddit's rate limits with built-in delays (~1 request/second)
- **Privacy-Focused**: All data is anonymized and aggregated locally
- **Non-Commercial**: Personal research use only, no monetization
- **Transparent**: Open-source code for full reviewer visibility

---

## Use Case

**Purpose**: Personal research into public health and wellness discussions, specifically tracking:
- Trending topics in peptide research communities
- Sentiment analysis of public discussions
- Volume patterns over time (weekly/monthly trends)
- Emerging subtopics and terminology

**Data Handling**:
- No personal user data is collected or stored
- Only publicly available post/comment text is analyzed
- Results are aggregated statistics (counts, percentages, sentiment scores)
- No data is shared, sold, or used commercially

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Reddit Public API                           │
│                   (via OAuth2 / PRAW)                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │ READ-ONLY
                      │ Rate-limited (1 req/sec)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Data Fetcher Module                           │
│         • Subreddit posts (new, hot, top)                      │
│         • Comments (limited depth)                              │
│         • Proper User-Agent identification                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Local Processing (Offline)                      │
│         • Text preprocessing                                    │
│         • Sentiment analysis (VADER/TextBlob)                  │
│         • Keyword extraction                                    │
│         • Trend aggregation                                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Local Storage (SQLite/CSV)                         │
│         • Anonymized aggregates only                           │
│         • No raw user data retained                            │
│         • Personal analysis files                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Reddit account
- Approved Reddit API credentials ([request here](https://www.reddit.com/prefs/apps))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dreday2050/reddit-peptide-trends.git
   cd reddit-peptide-trends
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure credentials**
   ```bash
   cp config.example.py config.py
   # Edit config.py with your Reddit API credentials
   ```

---

## Usage

```bash
# Fetch recent posts from target subreddits
python main.py

# Run with specific subreddit
python main.py --subreddit Peptides

# Analyze trends (after data collection)
python analyze.py
```

---

## Compliance

### Reddit API Terms Adherence

| Requirement | Implementation |
|-------------|----------------|
| **Rate Limiting** | Built-in 1-2 second delays between requests |
| **User-Agent** | Descriptive UA with version and contact info |
| **OAuth2** | Proper authentication via PRAW |
| **Read-Only** | Zero write endpoints used |
| **No Scraping** | Uses official API only |
| **Terms of Service** | Full compliance with Reddit ToS |

### What This Tool Does NOT Do

- Post, comment, vote, or interact with Reddit in any way
- Collect, store, or process personal user information
- Bypass rate limits or authentication
- Scrape data outside the official API
- Share or sell any collected data
- Operate for commercial purposes

See [COMPLIANCE.md](COMPLIANCE.md) for detailed compliance documentation.

---

## Project Status

**Current Phase**: Early development / Proof of concept

This repository demonstrates the intended architecture and compliance approach. Full functionality will be developed following API approval.

---

## File Structure

```
reddit-peptide-trends/
├── README.md              # This file
├── COMPLIANCE.md          # Detailed compliance documentation
├── LICENSE                # MIT License
├── requirements.txt       # Python dependencies
├── config.example.py      # Credential template (safe to commit)
├── main.py               # Main data fetcher script
├── analyze.py            # Trend analysis module
├── .gitignore            # Excludes secrets and cache
└── docs/
    └── data_flow.md      # Technical documentation
```

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## Contact

- **GitHub**: [@dreday2050](https://github.com/dreday2050)
- **Purpose**: Personal, non-commercial research
- **Questions**: Open an issue on this repository

---

## Acknowledgments

- [PRAW](https://praw.readthedocs.io/) - Python Reddit API Wrapper
- [Reddit API](https://www.reddit.com/dev/api/) - Official API documentation
- r/redditdev community for guidance on best practices

---

<p align="center">
  <i>Built with transparency and compliance in mind</i>
</p>
