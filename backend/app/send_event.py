import json

import boto3

client = boto3.client(
    "events",
    region_name="us-east-1",
)


def send_event_to_eventbridge(event_bus_name, source, detail_type, detail):
    response = client.put_events(
        Entries=[
            {
                "EventBusName": event_bus_name,
                "Source": source,
                "DetailType": detail_type,
                "Detail": json.dumps(detail),
            }
        ]
    )

    if response["FailedEntryCount"] > 0:
        print(f"Failed to send event: {response['Entries']}")
        raise Exception(f"Failed to send event: {response['Entries']}")
    elif response["FailedEntryCount"] == 0:
        print(f"Successfully sent event: {response['Entries']}")


if __name__ == "__main__":
    event_bus_name = "default"
    source = "email.lambda.caller"
    detail_type = "Random"
    detail = {"key1": "value1", "key2": "value2"}

    send_event_to_eventbridge(event_bus_name, source, detail_type, detail)
