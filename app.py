from aws_cdk import (
    App,
    Stack,
    aws_lambda as _lambda,

    )


from constructs import Construct


class AppStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        email_lambda = _lambda.DockerImageFunction(self, 'EmailLambda',
            code=_lambda.DockerImageCode.from_image_asset("./email_lambda"),   
            environment= {
                'SENDER_EMAIL': 'l', 
                'SENDER_PASSWORD':'l'
            },                         
        )



app = App()
AppStack(app, "AppStack")
app.synth()
