# config.py
# Central place for all pipeline parameters.
# Change values here instead of touching the main logic.

# --- NewsData.io ---
NEWSDATA_API_KEY = "pub_154cd54e6b19495d9db86d2f30f56332"
NEWSDATA_BASE_URL = "https://newsdata.io/api/1/news"
NEWS_LANGUAGE = "en"          # Language filter
NEWS_CATEGORY = "technology"  # Category to fetch (technology, business, sports, etc.)
NEWS_MAX_RESULTS = 50         # Max articles to fetch per run (free tier: up to 50)

# --- BigQuery ---
GCP_PROJECT_ID = "affable-framing-464607-b9"
BQ_DATASET_ID = "news_pipeline"
BQ_TABLE_ID = "articles"

# --- Keywords that flag an article as "breaking news" ---
BREAKING_KEYWORDS = ["breaking", "urgent", "alert", "just in", "developing", "exclusive"]

# --- Average reading speed (words per minute) ---
READING_SPEED_WPM = 200
