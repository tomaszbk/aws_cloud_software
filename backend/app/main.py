import psycopg2
from app.make_llm_query import submit_prompt
from app.models import Prompt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/retrieve-products")
async def retrieve_products(prompt: Prompt):
    query = submit_prompt(prompt.content)
    print(query)
    products = query_products(query)
    return {"products": products}


@app.post("/make_query")
def query_db(query: str):
    connection = psycopg2.connect(
        host=host, user=user, password=password, database=database
    )
    cursor = connection.cursor()

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


host = "ecommerce-database.cl0aei0o857j.us-west-2.rds.amazonaws.com"
user = "postgres"
password = "postgres"
database = "laptops_database"


def query_products(query):
    connection = psycopg2.connect(
        host=host, user=user, password=password, database=database
    )
    try:
        cursor = connection.cursor()

        cursor.execute(query.replace(";", " LIMIT 8;"))

        products = cursor.fetchall()

        cursor.close()
        connection.close()

        return products

    except Exception as e:
        print(f"error {e}")
        return []
