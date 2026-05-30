# transform.py
# Cleans raw API data and adds meaningful derived fields.

import logging
from datetime import datetime, timezone
from config import BREAKING_KEYWORDS, READING_SPEED_WPM

logger = logging.getLogger(__name__)


def _estimate_reading_time(text: str) -> int:
    """
    Estimates reading time in seconds based on word count.
    Uses average reading speed defined in config.
    """
    if not text or not isinstance(text, str):
        return 0
    word_count = len(text.split())
    reading_time_seconds = round((word_count / READING_SPEED_WPM) * 60)
    return reading_time_seconds


def _is_breaking_news(title: str) -> bool:
    """
    Returns True if the article title contains any breaking news keywords.
    Case-insensitive check.
    """
    if not title or not isinstance(title, str):
        return False
    title_lower = title.lower()
    return any(keyword in title_lower for keyword in BREAKING_KEYWORDS)


def _clean_string(value) -> str:
    """
    Returns a clean string or empty string if value is None or not a string.
    """
    if value is None:
        return ""
    return str(value).strip()


def _clean_list(value) -> str:
    """
    Converts a list (like keywords or categories) into a comma-separated string.
    BigQuery handles plain strings more simply than arrays in sandbox mode.
    """
    if isinstance(value, list):
        return ", ".join([str(v) for v in value if v])
    if isinstance(value, str):
        return value.strip()
    return ""


def transform_articles(raw_articles: list[dict]) -> list[dict]:
    """
    Takes raw articles from the API and returns a cleaned, enriched list
    ready to be loaded into BigQuery.
    """
    if not raw_articles:
        logger.warning("No articles to transform.")
        return []

    transformed = []
    skipped = 0

    for article in raw_articles:
        # Skip articles with no title or article_id — they are not useful
        if not article.get("title") or not article.get("article_id"):
            skipped += 1
            continue

        title = _clean_string(article.get("title"))
        description = _clean_string(article.get("description"))
        content = _clean_string(article.get("content"))

        # Use description for reading time if content is not available
        text_for_reading = content if content else description

        transformed_article = {
            # --- Core fields ---
            "article_id":         _clean_string(article.get("article_id")),
            "title":              title,
            "description":        description,
            "source_name":        _clean_string(article.get("source_id")),
            "source_url":         _clean_string(article.get("link")),
            "author":             _clean_list(article.get("creator")),
            "language":           _clean_string(article.get("language")),
            "country":            _clean_list(article.get("country")),
            "category":           _clean_list(article.get("category")),
            "keywords":           _clean_list(article.get("keywords")),
            "image_url":          _clean_string(article.get("image_url")),
            "published_at":       _clean_string(article.get("pubDate")),

            # --- Derived fields (added by our pipeline) ---
            "reading_time_seconds": _estimate_reading_time(text_for_reading),
            "is_breaking_news":     _is_breaking_news(title),
            "has_image":            bool(article.get("image_url")),
            "has_description":      bool(description),
            "ingested_at":          datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        }

        transformed.append(transformed_article)

    logger.info(f"Transformed {len(transformed)} articles. Skipped {skipped} incomplete articles.")
    return transformed
