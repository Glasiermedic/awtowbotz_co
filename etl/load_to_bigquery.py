import os  # Allowing interaction with operating system
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv
from pathlib import Path

# Base project directory and CSV path
BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data" / "transformer_sales.csv"

# Load environment variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# GCP and BigQuery config
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET")
TABLE_ID = "transformer_sales"
FULL_TABLE = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# Read CSV
df = pd.read_csv(csv_path)

# Add calculated column
df["total_sale"] = df["units_sold"] * df["unit_price"]

# Enforce schema types
df["sale_date"] = pd.to_datetime(df["sale_date"])

# Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)

# Define BigQuery schema
schema = [
    bigquery.SchemaField("order_id", "INTEGER"),
    bigquery.SchemaField("product_type", "STRING"),
    bigquery.SchemaField("region", "STRING"),
    bigquery.SchemaField("sales_rep", "STRING"),
    bigquery.SchemaField("units_sold", "INTEGER"),
    bigquery.SchemaField("unit_price", "FLOAT"),
    bigquery.SchemaField("sale_date", "DATE"),
    bigquery.SchemaField("total_sale", "FLOAT"),
]

# Load into BigQuery
job_config = bigquery.LoadJobConfig(schema=schema, write_disposition="WRITE_TRUNCATE")
job = client.load_table_from_dataframe(df, FULL_TABLE, job_config=job_config)
job.result()

print(f"✅ Loaded {len(df)} rows into {FULL_TABLE}")
