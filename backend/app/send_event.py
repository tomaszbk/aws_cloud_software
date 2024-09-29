import json

import boto3

client = boto3.client(
    "events",
    region_name="us-east-1",
)


def send_event_to_eventbridge(destiny_email: str):
    event_detail = {
        'destiny_email': destiny_email  # This matches the Go Lambda's struct
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
