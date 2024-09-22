from aws_cdk import (
    App,
    Stack,
)
from aws_cdk import (
    aws_lambda as _lambda,
)
from constructs import Construct
import os

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")

class AppStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        email_lambda = _lambda.DockerImageFunction(
            self,
            "EmailLambda",
            code=_lambda.DockerImageCode.from_image_asset("./email_lambda"),
            environment={"SENDER_EMAIL": SENDER_EMAIL, "SENDER_PASSWORD": SENDER_PASSWORD},
        )


app = App()
AppStack(app, "AppStack")
app.synth()
