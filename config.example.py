"""
Configuration Template
======================

Copy this file to config.py and fill in your Reddit API credentials.

To obtain credentials:
1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app..."
3. Select "script" for personal use
4. Fill in name and description
5. Use http://localhost:8080 as redirect URI
6. Copy the client_id (under app name) and client_secret

SECURITY NOTICE:
- NEVER commit config.py to version control
- config.py is listed in .gitignore for safety
- Keep your credentials private
"""

# ============================================================================
# REDDIT API CREDENTIALS
# ============================================================================

# Your Reddit App's client ID (found under the app name on reddit.com/prefs/apps)
REDDIT_CLIENT_ID = "YOUR_CLIENT_ID_HERE"

# Your Reddit App's client secret
REDDIT_CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"

# User-Agent string (REQUIRED by Reddit API)
# Format: <platform>:<app_name>:<version> (by u/<reddit_username>)
# Example: "python:peptide-trend-analyzer:v0.1 (by u/your_username)"
REDDIT_USER_AGENT = "python:peptide-trend-analyzer:v0.1 (by u/YOUR_REDDIT_USERNAME) - read-only research tool"

# ============================================================================
# OPTIONAL SETTINGS
# ============================================================================

# Database path for storing anonymized aggregates (local SQLite)
DATABASE_PATH = "data/trends.db"

# Output directory for analysis results
OUTPUT_DIR = "output/"

# Logging level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"
