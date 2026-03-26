import duckdb
import os
from google.cloud import storage

def process_and_upload(year, bucket_name):
    input_file = f"data/services-{year}.csv.gz"
    output_parquet = f"data/services-{year}.parquet"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Converting {year} data...")
    # SQL inside DuckDB for high-speed conversion
    duckdb.query(f"COPY (SELECT * FROM read_csv_auto('{input_file}')) TO '{output_parquet}' (FORMAT 'PARQUET')")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"raw/services-{year}.parquet")
    blob.upload_from_filename(output_parquet)
    print(f"Uploaded {year} data to GCS.")

if __name__ == "__main__":
    MY_BUCKET = "railway-data-lake-dammi-2026"
    
    # Circuit Breaker: Verify cloud access before starting the loop
    try:
        client = storage.Client()
        client.get_bucket(MY_BUCKET)
        print("Cloud connection verified.")
    except Exception as e:
        print(f"Cloud connection failed: {e}")
        exit(1)

    for yr in [2024, 2025]:
        process_and_upload(yr, MY_BUCKET)        
