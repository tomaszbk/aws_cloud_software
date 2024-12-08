import json

import boto3

from app.config import cfg

client = boto3.client(
    "events",
    region_name=cfg.AWS_REGION,
)


def send_event_to_eventbridge(destiny_email: str, user_name: str, product_image_url: str):
    event_detail = {
        "destiny_email": destiny_email,  # This matches the Go Lambda's struct
        "destiny_name": user_name,
        "product_image_url": product_image_url,
    }
    response = client.put_events(
        Entries=[
            {
                "EventBusName": "default",
                "Source": "fastapi.backend",
                "DetailType": "EmailEvent",
                "Detail": json.dumps(event_detail),
            }
        ]
    )

    if response["FailedEntryCount"] > 0:
        print(f"Failed to send event: {response['Entries']}")
        raise Exception(f"Failed to send event: {response['Entries']}")
    elif response["FailedEntryCount"] == 0:
        print(f"Successfully sent event: {response['Entries']}")
