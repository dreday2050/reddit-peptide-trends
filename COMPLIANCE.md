# Reddit API Compliance Documentation

This document details how this project complies with Reddit's API Terms of Use, Data API Terms, and Responsible Builder Policy.

---

## Summary

| Aspect | Status | Details |
|--------|--------|---------|
| **Operation Mode** | Read-Only | No write operations of any kind |
| **Rate Limiting** | Compliant | 1-2 second delays between requests |
| **Authentication** | OAuth2 | Proper PRAW authentication |
| **User-Agent** | Compliant | Descriptive, versioned, with contact |
| **Data Usage** | Personal | Non-commercial research only |
| **Privacy** | Protected | No PII collected or stored |
| **Commercial Use** | None | Zero monetization |

---

## Detailed Compliance

### 1. Read-Only Operations

This application **exclusively** uses read-only API endpoints:

**Endpoints Used:**
- `GET /r/{subreddit}/new` - Fetch new posts
- `GET /r/{subreddit}/hot` - Fetch hot posts
- `GET /r/{subreddit}/top` - Fetch top posts

**Endpoints NOT Used (and never will be):**
- `POST /api/submit` - Create posts
- `POST /api/comment` - Post comments
- `POST /api/vote` - Vote on content
- `POST /api/subscribe` - Subscribe to subreddits
- Any moderation endpoints
- Any user account modification endpoints

The code explicitly runs PRAW without username/password credentials, ensuring the client operates in read-only mode. This is verified at runtime:

```python
if not reddit.read_only:
    logger.error("Client is not in read-only mode. Exiting for safety.")
    return
```

### 2. Rate Limiting

We implement conservative rate limiting that stays well within Reddit's guidelines:

- **Reddit's Limit**: ~60 requests per minute (1 per second)
- **Our Implementation**: ~30 requests per minute (2-second delay)

```python
REQUEST_DELAY_SECONDS = 2.0
# ...
time.sleep(REQUEST_DELAY_SECONDS)  # After each request
```

This 50% buffer ensures we never approach rate limits, even with network variability.

### 3. User-Agent Identification

Our User-Agent follows Reddit's required format:

```
python:peptide-trend-analyzer:v0.1 (by u/[username]) - read-only research tool
```

Components:
- **Platform**: `python`
- **App Name**: `peptide-trend-analyzer`
- **Version**: `v0.1`
- **Contact**: Reddit username
- **Purpose**: Clarifies read-only research intent

### 4. Authentication

- Uses OAuth2 via PRAW (Reddit's official Python wrapper)
- Application-only authentication (no user login)
- Credentials stored securely (excluded from version control via `.gitignore`)

### 5. Data Handling & Privacy

**What We Collect:**
- Post titles and body text (public data)
- Engagement metrics (score, comment count, upvote ratio)
- Timestamps
- Subreddit names

**What We DO NOT Collect:**
- Usernames or author information
- User IDs or account data
- Private messages or private subreddit content
- Any personally identifiable information (PII)

**Data Storage:**
- All data stored locally only
- No cloud uploads or external transmission
- No data sharing with third parties
- Data used solely for personal trend analysis

### 6. Non-Commercial Use

This project is:
- **Personal research** - Understanding public discussion trends
- **Non-monetized** - No ads, subscriptions, or sales
- **Open source** - Full transparency of code and intent
- **Educational** - Learning about API usage and data analysis

We do not and will not:
- Sell or license collected data
- Use data for commercial products
- Monetize insights or analysis
- Provide data to commercial entities

### 7. Terms of Service Compliance

This project adheres to:
- [Reddit API Terms of Use](https://www.redditinc.com/policies/data-api-terms)
- [Reddit User Agreement](https://www.redditinc.com/policies/user-agreement)
- [Reddit Privacy Policy](https://www.reddit.com/policies/privacy-policy)
- [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)

---

## Contact

For questions about this project's compliance:
- **GitHub Issues**: Open an issue on this repository
- **Reddit**: Contact via Reddit username listed in User-Agent

---

## Changelog

| Date | Change |
|------|--------|
| 2025-01 | Initial compliance documentation |

---

*This document is maintained as part of our commitment to transparency and responsible API usage.*
