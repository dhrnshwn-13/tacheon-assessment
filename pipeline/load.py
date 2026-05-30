# load.py
# Responsible for creating the BigQuery table (if needed) and loading data into it.

import csv
import logging
import os
import tempfile
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPICallError
from config import GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID

logger = logging.getLogger(__name__)

TABLE_REF = f"{GCP_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_ID}"


def get_bq_client() -> bigquery.Client:
    return bigquery.Client(project=GCP_PROJECT_ID)


def get_schema():
    return [
        bigquery.SchemaField("article_id",           "STRING"),
        bigquery.SchemaField("title",                "STRING"),
        bigquery.SchemaField("description",          "STRING"),
        bigquery.SchemaField("source_name",          "STRING"),
        bigquery.SchemaField("source_url",           "STRING"),
        bigquery.SchemaField("author",               "STRING"),
        bigquery.SchemaField("language",             "STRING"),
        bigquery.SchemaField("country",              "STRING"),
        bigquery.SchemaField("category",             "STRING"),
        bigquery.SchemaField("keywords",             "STRING"),
        bigquery.SchemaField("image_url",            "STRING"),
        bigquery.SchemaField("published_at",         "STRING"),
        bigquery.SchemaField("reading_time_seconds", "INTEGER"),
        bigquery.SchemaField("is_breaking_news",     "BOOLEAN"),
        bigquery.SchemaField("has_image",            "BOOLEAN"),
        bigquery.SchemaField("has_description",      "BOOLEAN"),
        bigquery.SchemaField("ingested_at",          "STRING"),
    ]


def ensure_table_exists(client: bigquery.Client):
    dataset_ref = bigquery.Dataset(f"{GCP_PROJECT_ID}.{BQ_DATASET_ID}")
    dataset_ref.location = "US"
    try:
        client.create_dataset(dataset_ref, exists_ok=True)
        logger.info(f"Dataset '{BQ_DATASET_ID}' is ready.")
    except GoogleAPICallError as e:
        logger.error(f"Failed to create dataset: {e}")
        raise

    table = bigquery.Table(TABLE_REF, schema=get_schema())
    try:
        client.create_table(table, exists_ok=True)
        logger.info(f"Table '{TABLE_REF}' is ready.")
    except GoogleAPICallError as e:
        logger.error(f"Failed to create table: {e}")
        raise


def load_to_bigquery(articles: list[dict]) -> bool:
    if not articles:
        logger.warning("No articles to load into BigQuery.")
        return False

    try:
        client = get_bq_client()
        ensure_table_exists(client)

        # Write to a temp CSV file then batch load into BigQuery
        # (Streaming inserts are not allowed in BigQuery Sandbox free tier)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=articles[0].keys())
            writer.writeheader()
            writer.writerows(articles)
            tmp_path = f.name

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=False,
            schema=get_schema(),
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        with open(tmp_path, "rb") as f:
            job = client.load_table_from_file(f, TABLE_REF, job_config=job_config)

        job.result()  # Wait for job to complete
        os.remove(tmp_path)  # Clean up temp file

        logger.info(f"Successfully loaded {len(articles)} articles into '{TABLE_REF}'.")
        return True

    except GoogleAPICallError as e:
        logger.error(f"BigQuery API error: {e}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error during BigQuery load: {e}")
        return False