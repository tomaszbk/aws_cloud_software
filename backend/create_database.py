import psycopg2

# Database connection details
host = "ecommerce-database.cl0aei0o857j.us-west-2.rds.amazonaws.com"
user = "postgres"
password = "postgres"
database = "laptops_database"


try:
    # Connect to the database
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        #  database=database
    )
    connection.autocommit = True
    # Create a cursor object
    cursor = connection.cursor()

    # Create the database
    cursor.execute(f"CREATE DATABASE {database}")

    # Commit the changes
    connection.commit()

    # Close the cursor
    cursor.close()
    connection.close()

except Exception as e:
    print(f"error {e}")
