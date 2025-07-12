import os
from google.cloud import bigquery
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Explicitly provide the project ID
project_id = os.getenv("GCP_PROJECT_ID")
client = bigquery.Client(project=project_id)

query = f"SELECT COUNT(*) AS total_rows FROM `{project_id}.autobotz_dataset.transformer_sales`"
result = client.query(query).result()

for row in result:
    print("✅ Total rows in transformer_sales:", row["total_rows"])