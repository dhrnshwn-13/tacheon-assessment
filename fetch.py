# fetch.py
# Responsible for calling the NewsData.io API and returning raw articles.

import requests
import logging
from config import (
    NEWSDATA_API_KEY,
    NEWSDATA_BASE_URL,
    NEWS_LANGUAGE,
    NEWS_CATEGORY,
    NEWS_MAX_RESULTS,
)

# Set up logging so we can see what's happening when the script runs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def fetch_news() -> list[dict]:
    """
    Fetches news articles from NewsData.io.
    Returns a list of raw article dictionaries.
    Returns an empty list if anything goes wrong.
    """
    params = {
        "apikey": NEWSDATA_API_KEY,
        "language": NEWS_LANGUAGE,
        "category": NEWS_CATEGORY,
    }

    logger.info(f"Fetching news from NewsData.io | category={NEWS_CATEGORY}, language={NEWS_LANGUAGE}")

    try:
        response = requests.get(NEWSDATA_BASE_URL, params=params, timeout=15)

        # Raise an error if the status code is 4xx or 5xx
        response.raise_for_status()

        data = response.json()

        # Check if the API returned a success status
        if data.get("status") != "success":
            logger.error(f"API returned non-success status: {data.get('status')} | Message: {data.get('message')}")
            return []

        articles = data.get("results", [])
        logger.info(f"Successfully fetched {len(articles)} articles.")
        return articles

    except requests.exceptions.ConnectionError:
        logger.error("Connection error: Could not reach NewsData.io. Check your internet connection.")
        return []

    except requests.exceptions.Timeout:
        logger.error("Request timed out: NewsData.io took too long to respond.")
        return []

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return []

    except Exception as e:
        logger.error(f"Unexpected error during fetch: {e}")
        return []
