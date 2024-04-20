import boto3
import pandas as pd
from sqlalchemy import create_engine

# Database connection details
host = "ecommerce-database.cl0aei0o857j.us-west-2.rds.amazonaws.com"
user = "postgres"
password = "postgres"
database = "laptops_database"


try:
    s3 = boto3.client("s3")
    bucket_name = "ecommerce-laptops-data"
    file_name = "laptops.csv"

    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    data = pd.read_csv(obj["Body"])

    table_name = "laptops"

    engine = create_engine(f"postgresql://{user}:{password}@{host}/{database}")

    data.to_sql(table_name, engine, if_exists="replace", index=False)

    engine.dispose()

except Exception as e:
    print(f"error {e}")
