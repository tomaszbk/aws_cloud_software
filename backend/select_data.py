from sqlalchemy import create_engine, text

host = "ecommerce-database.cl0aei0o857j.us-west-2.rds.amazonaws.com"
user = "postgres"
password = "postgres"
database = "laptops_database"

sql_query = text("SELECT * FROM laptops LIMIT 15;")


engine = create_engine(f"postgresql://{user}:{password}@{host}/{database}")

with engine.connect() as connection:
    result = connection.execute(sql_query)

    for row in result:
        print(row)
