# load.py
# Responsible for creating the BigQuery table (if needed) and loading data into it.

import logging
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPICallError
from config import GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID

logger = logging.getLogger(__name__)

# Full table reference string
TABLE_REF = f"{GCP_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_ID}"


def get_bq_client() -> bigquery.Client:
    """Creates and returns a BigQuery client."""
    return bigquery.Client(project=GCP_PROJECT_ID)


def ensure_table_exists(client: bigquery.Client):
    """
    Creates the BigQuery dataset and table if they don't already exist.
    Safe to run every time — won't overwrite existing data.
    """
    # Create dataset if it doesn't exist
    dataset_ref = bigquery.Dataset(f"{GCP_PROJECT_ID}.{BQ_DATASET_ID}")
    dataset_ref.location = "US"
    try:
        client.create_dataset(dataset_ref, exists_ok=True)
        logger.info(f"Dataset '{BQ_DATASET_ID}' is ready.")
    except GoogleAPICallError as e:
        logger.error(f"Failed to create dataset: {e}")
        raise

    # Define the table schema
    schema = [
        bigquery.SchemaField("article_id",            "STRING",    mode="REQUIRED"),
        bigquery.SchemaField("title",                 "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("description",           "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("source_name",           "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("source_url",            "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("author",                "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("language",              "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("country",               "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("category",              "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("keywords",              "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("image_url",             "STRING",    mode="NULLABLE"),
        bigquery.SchemaField("published_at",          "STRING",    mode="NULLABLE"),

        # Derived fields
        bigquery.SchemaField("reading_time_seconds",  "INTEGER",   mode="NULLABLE"),
        bigquery.SchemaField("is_breaking_news",      "BOOLEAN",   mode="NULLABLE"),
        bigquery.SchemaField("has_image",             "BOOLEAN",   mode="NULLABLE"),
        bigquery.SchemaField("has_description",       "BOOLEAN",   mode="NULLABLE"),
        bigquery.SchemaField("ingested_at",           "STRING",    mode="NULLABLE"),
    ]

    table = bigquery.Table(TABLE_REF, schema=schema)

    try:
        client.create_table(table, exists_ok=True)
        logger.info(f"Table '{TABLE_REF}' is ready.")
    except GoogleAPICallError as e:
        logger.error(f"Failed to create table: {e}")
        raise


def load_to_bigquery(articles: list[dict]) -> bool:
    """
    Loads transformed articles into BigQuery.
    Returns True if successful, False otherwise.
    """
    if not articles:
        logger.warning("No articles to load into BigQuery.")
        return False

    try:
        client = get_bq_client()
        ensure_table_exists(client)

        # Insert rows into BigQuery
        errors = client.insert_rows_json(TABLE_REF, articles)

        if errors:
            logger.error(f"BigQuery insert errors: {errors}")
            return False

        logger.info(f"Successfully loaded {len(articles)} articles into '{TABLE_REF}'.")
        return True

    except GoogleAPICallError as e:
        logger.error(f"BigQuery API error: {e}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error during BigQuery load: {e}")
        return False
