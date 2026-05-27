# main.py
# The entry point. Run this file to execute the full pipeline.
# It ties together fetch → transform → load.

import logging
import sys
from fetch import fetch_news
from transform import transform_articles
from load import load_to_bigquery

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("=== Pipeline started ===")

    # Step 1: Fetch
    logger.info("Step 1: Fetching data from NewsData.io...")
    raw_articles = fetch_news()

    if not raw_articles:
        logger.error("No articles fetched. Stopping pipeline.")
        sys.exit(1)

    # Step 2: Transform
    logger.info("Step 2: Transforming articles...")
    transformed_articles = transform_articles(raw_articles)

    if not transformed_articles:
        logger.error("No articles after transformation. Stopping pipeline.")
        sys.exit(1)

    # Step 3: Load
    logger.info("Step 3: Loading into BigQuery...")
    success = load_to_bigquery(transformed_articles)

    if success:
        logger.info("=== Pipeline completed successfully ===")
    else:
        logger.error("=== Pipeline finished with errors ===")
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()
