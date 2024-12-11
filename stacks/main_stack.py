import os

from aws_cdk import (
    App,
    RemovalPolicy,
    Stack,
)
from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_dynamodb as ddb,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_s3 as s3,
)
from constructs import Construct
import os

from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")


class MainStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        email_lambda = _lambda.DockerImageFunction(
            self,
            "EmailLambda",
            code=_lambda.DockerImageCode.from_image_asset(directory="./email_lambda"),
            environment={"SENDER_EMAIL": SENDER_EMAIL, "SENDER_PASSWORD": SENDER_PASSWORD},
        )

        
       
        event_rule = events.Rule(
            self,
            id="EmailNotificationRule",
            event_pattern=events.EventPattern(
                source=["fastapi.backend"], detail_type=["EmailEvent"]
            ),
        )
        # Add the Lambda function as a target to the EventBridge rule
        event_rule.add_target(events_targets.LambdaFunction(email_lambda,
                                                            event=events.RuleTargetInput.from_object(
                                                                {
                                                                "destiny_email": events.EventField.from_path("$.detail.destiny_email"),
                                                                "destiny_name": events.EventField.from_path("$.detail.destiny_name"),
                                                                "product_image_url": events.EventField.from_path("$.detail.product_image_url"),
                                                                 }
                                                                 )))

