from app.database.dynamo_config import dynamodb

# Create a new table
table = dynamodb.create_table(
    TableName="Users",
    KeySchema=[
        {
            "AttributeName": "UserId",
            "KeyType": "HASH",  # Partition key
        },
    ],
    AttributeDefinitions=[
        {
            "AttributeName": "UserId",
            "AttributeType": "S",  # String
        },
    ],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)

# Wait until the table is created
table.meta.client.get_waiter("table_exists").wait(TableName="Users")

print(f"Table status: {table.table_status}")
