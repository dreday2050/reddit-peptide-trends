# Data Flow Documentation

This document describes how data flows through the Reddit Peptide Trend Analyzer.

---

## Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INTERNET                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     Reddit Public API                                │    │
│  │                   api.reddit.com                                     │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │    │
│  │  │ /r/sub/new  │  │ /r/sub/hot  │  │ /r/sub/top  │                  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                  │    │
│  └──────────────────────────┬──────────────────────────────────────────┘    │
└─────────────────────────────┼───────────────────────────────────────────────┘
                              │
                              │ HTTPS (OAuth2)
                              │ READ-ONLY
                              │ Rate Limited: 1 req / 2 sec
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LOCAL MACHINE                                      │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        main.py                                       │    │
│  │                   (Data Fetcher Module)                              │    │
│  │                                                                      │    │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │    │
│  │   │ PRAW Client  │───▶│ Rate Limiter │───▶│ Data Extract │         │    │
│  │   │ (OAuth2)     │    │ (2s delay)   │    │ (Anonymize)  │         │    │
│  │   └──────────────┘    └──────────────┘    └──────────────┘         │    │
│  │                                                   │                  │    │
│  └───────────────────────────────────────────────────┼──────────────────┘    │
│                                                      │                       │
│                                                      ▼                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     Local Storage                                    │    │
│  │                                                                      │    │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │    │
│  │   │  data/*.db   │    │ output/*.csv │    │   Logs       │         │    │
│  │   │  (SQLite)    │    │ (Analysis)   │    │              │         │    │
│  │   └──────────────┘    └──────────────┘    └──────────────┘         │    │
│  │         │                    │                                      │    │
│  └─────────┼────────────────────┼──────────────────────────────────────┘    │
│            │                    │                                            │
│            ▼                    ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      analyze.py                                      │    │
│  │                  (Analysis Module)                                   │    │
│  │                                                                      │    │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │    │
│  │   │  Sentiment   │    │   Keyword    │    │    Trend     │         │    │
│  │   │  Analysis    │    │  Extraction  │    │   Metrics    │         │    │
│  │   └──────────────┘    └──────────────┘    └──────────────┘         │    │
│  │                                                   │                  │    │
│  └───────────────────────────────────────────────────┼──────────────────┘    │
│                                                      │                       │
│                                                      ▼                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    Personal Analysis                                 │    │
│  │              (Charts, Reports, Insights)                            │    │
│  │                    NEVER SHARED                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Steps

### Step 1: API Request

```
User runs main.py
       │
       ▼
┌─────────────────┐
│ Initialize PRAW │
│ - OAuth2 auth   │
│ - Read-only     │
│ - User-Agent    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Request Data    │
│ - GET only      │
│ - Public posts  │
│ - Rate limited  │
└─────────────────┘
```

### Step 2: Data Extraction

```
Raw API Response
       │
       ▼
┌─────────────────────────────────────┐
│         Extract Public Data          │
├─────────────────────────────────────┤
│ INCLUDED:          │ EXCLUDED:       │
│ - Post ID          │ - Author name   │
│ - Title            │ - User ID       │
│ - Body text        │ - User history  │
│ - Score            │ - Private data  │
│ - Comment count    │ - PII           │
│ - Timestamp        │                 │
│ - Subreddit        │                 │
└─────────────────────────────────────┘
```

### Step 3: Local Storage

```
Extracted Data
       │
       ▼
┌─────────────────┐
│ Local Database  │
│ (SQLite)        │
│                 │
│ - Anonymized    │
│ - Local only    │
│ - Not shared    │
└─────────────────┘
```

### Step 4: Analysis (Offline)

```
Stored Data
       │
       ▼
┌─────────────────────────────────────┐
│           Local Analysis             │
│         (No API calls)               │
├─────────────────────────────────────┤
│ - Sentiment scoring                  │
│ - Keyword frequency                  │
│ - Trend calculations                 │
│ - Volume over time                   │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────┐
│ Personal Use    │
│ - View trends   │
│ - Research      │
│ - Learning      │
└─────────────────┘
```

---

## Security Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY BOUNDARY                             │
│                                                                  │
│  ┌────────────────┐      ┌────────────────┐                     │
│  │   config.py    │      │    .env        │                     │
│  │  (GITIGNORED)  │      │  (GITIGNORED)  │                     │
│  │                │      │                │                     │
│  │ - client_id    │      │ - secrets      │                     │
│  │ - client_secret│      │ - API keys     │                     │
│  └────────────────┘      └────────────────┘                     │
│                                                                  │
│  These files NEVER leave local machine                          │
│  These files are NEVER committed to git                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## What Happens to Data

| Data Type | Collection | Storage | Sharing | Retention |
|-----------|------------|---------|---------|-----------|
| Post titles | Yes | Local DB | Never | Until deleted |
| Post body | Yes (truncated) | Local DB | Never | Until deleted |
| Scores | Yes | Local DB | Never | Until deleted |
| Timestamps | Yes | Local DB | Never | Until deleted |
| Usernames | **NO** | N/A | N/A | N/A |
| User IDs | **NO** | N/A | N/A | N/A |
| Private content | **NO** | N/A | N/A | N/A |

---

## Network Connections

This application makes **exactly one type** of network connection:

| Direction | Destination | Purpose | Protocol | Frequency |
|-----------|-------------|---------|----------|-----------|
| Outbound | api.reddit.com | Fetch public posts | HTTPS | ~30 req/min max |

**No other network connections are made.**

---

*Document version: 1.0*
*Last updated: January 2025*
