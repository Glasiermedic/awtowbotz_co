### Designed to be used once to replace the temporary static data with a more random and realistic dataset for a company that specializes in "transformers"
### The original data was intended to make it easier to visualize, easy to see in BigQuery and very easy to create reports in Google Sheets.

import os
import random
from datetime import datetime, timedelta
from google.cloud import bigquery
from dotenv import load_dotenv
import pandas as pd

# Load env variables
load_dotenv()
client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))
TABLE_ID = f"{os.getenv('GCP_PROJECT_ID')}.{os.getenv('BQ_DATASET')}.transformer_sales"
FULL_TABLE = TABLE_ID

SALES_REPS = ['Ava', 'Carlos', 'John', 'Lisa', 'Mary', 'Noah']
SALES_WEIGHTS = [0.25, 0.25, 0.25, 0.1, 0.1, 0.05]
REGIONS = ['US-East', 'US-North', 'US-South', 'US-West', 'CA', 'EUR', 'AFR-North', 'AFR-South',
           'AUS', 'PAC-Islands', 'RUS', 'CHIN', 'JPN', 'AMER-South', 'AMER-Central']
PRODUCT_TYPES = ['Cast Resin', 'Dry-Type', 'Oil-Insulated', 'Padmount', 'Substation', 'Switchgear', 'Three-Phase']
PREFERRED_UNITS = [1, 2, 4, 5, 7, 3]
PREFERRED_WEIGHTS = [0.2, 0.18, 0.16, 0.14, 0.12, 0.1]
OTHER_UNITS = list(range(8, 26))
OTHER_WEIGHTS = [0.01] * len(OTHER_UNITS)
UNIT_OPTIONS = PREFERRED_UNITS + OTHER_UNITS
UNIT_WEIGHTS = PREFERRED_WEIGHTS + OTHER_WEIGHTS

def generate_transaction(timestamp, order_id):
    units_sold = random.choices(UNIT_OPTIONS, weights=UNIT_WEIGHTS, k=1)[0]
    unit_price = round(random.uniform(3000, 15000), 2)
    total_sale = round(units_sold * unit_price, 2)
    return {
        'order_id': order_id,
        'sale_timestamp': timestamp.isoformat(),
        'sale_date': timestamp.date().isoformat(),
        'sales_rep': random.choices(SALES_REPS, weights=SALES_WEIGHTS, k=1)[0],
        'region': random.choice(REGIONS),
        'product_type': random.choice(PRODUCT_TYPES),
        'units_sold': units_sold,
        'unit_price': unit_price,
        'total_sale': total_sale
    }

def main():
    # Delete all rows in the table
    client.query(f"DELETE FROM `{TABLE_ID}` WHERE TRUE").result()
    print("🧨 Existing data wiped.")

    # Get the max order_id already in the table (default to 0)
    query = f"SELECT MAX(order_id) AS max_id FROM `{TABLE_ID}`"
    result = client.query(query).result()
    row = next(result)
    order_id = (row.max_id or 0) + 1

    start_date = datetime(2023, 7, 1)
    end_date = datetime(2025, 7, 12)
    inserts = []

    current = start_date
    while current <= end_date:
        for hour in range(3, 20):  # only add new data if hour within window of 3AM–7PM
            base_time = current.replace(hour=hour, minute=0, second=0, microsecond=0)
            for _ in range(random.randint(1, 4)):
                inserts.append(generate_transaction(base_time, order_id))
                order_id += 1
        current += timedelta(days=1)

    # Save full dataframe to CSV
    df = pd.DataFrame(inserts)
    csv_output_path = os.path.join(os.path.dirname(__file__), "generated_sales_data.csv")
    df.to_csv(csv_output_path, index=False)
    print(f"📄 Data exported to CSV at: {csv_output_path}")

    # Upload to BigQuery in chunks
    chunk_size = 1000
    for i in range(0, len(inserts), chunk_size):
        chunk = inserts[i:i + chunk_size]
        errors = client.insert_rows_json(TABLE_ID, chunk)
        if errors:
            print(f"❌ Errors in rows {i}–{i + chunk_size}:")
            for error in errors:
                print(error)
        else:
            print(f"✅ Inserted rows {i} to {i + chunk_size}")

    print(f"🧾 Using full table: {FULL_TABLE}")
    print("🎉 Full data replacement complete.")
    print("👤 Using credentials from:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    print("📁 Project ID:", os.getenv('GCP_PROJECT_ID'))

if __name__ == "__main__":
    main()