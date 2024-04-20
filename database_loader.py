import boto3
import pandas as pd
import psycopg2

# Connect to the RDS instance
conn = psycopg2.connect(
    host="ecommerce-database.cl0aei0o857j.us-west-2.rds.amazonaws.com",
    port="5432",
    # database="laptop_database",
    user="postgres",
    password="postgres",
)

s3 = boto3.client("s3")
bucket_name = "ecommerce-laptops-data"
file_key = "laptops.csv"
response = s3.get_object(Bucket=bucket_name, Key=file_key)
status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

if status == 200:
    data = response["Body"].read().decode("utf-8")
    df = pd.read_csv(pd.compat.StringIO(data))
else:
    print(f"Failed to get file: {file_key}")

df.to_sql("laptops", conn, if_exists="replace", index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()
