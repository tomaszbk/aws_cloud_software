from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_dynamodb as ddb,
)
from constructs import Construct

class StorageStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.image_bucket = s3.Bucket(self, "ProductImages",
            bucket_name="product-images-utn-frlp",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,)

        self.products_table = ddb.Table(
            self, 'ProductsTable',
            table_name='products',
            partition_key={'name': 'product_id', 'type': ddb.AttributeType.STRING},
            sort_key={'name': 'category', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )

        self.users_table = ddb.Table(
            self, 'UsersTable',
            table_name='users',
            partition_key={'name': 'phone_number', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )
