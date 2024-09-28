from aws_cdk import (
    App,
    Stack,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_s3 as s3,
    aws_dynamodb as ddb,
    aws_iam as iam
)

from constructs import Construct
import os
from dotenv import load_dotenv

load_dotenv()
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
class AppStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        
        email_lambda = _lambda.DockerImageFunction(
            self,
            "EmailLambda",
            code=_lambda.DockerImageCode.from_image_asset(directory="./email_lambda"),
            environment={"SENDER_EMAIL": SENDER_EMAIL, "SENDER_PASSWORD": SENDER_PASSWORD},
        )

        image_bucket = s3.Bucket(self, "product-images", 
            bucket_name="product-images", 
            removal_policy=RemovalPolicy.DESTROY)

        products_table = ddb.Table(
            self, 'ProductsTable',
            table_name='products',
            partition_key={'name': 'category', 'type': ddb.AttributeType.STRING},
            sort_key={'name': 'product_id', 'type': ddb.AttributeType.NUMBER},
            removal_policy=RemovalPolicy.DESTROY
        )
        
        users_table = ddb.Table(
            self, 'UsersTable',
            table_name='products',
            partition_key={'name': 'phone_number', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create an IAM Role for ECS Task Definition
        ecs_task_role = iam.Role(self, "ECSTaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )

        image_bucket.grant_read_write(ecs_task_role)
        users_table.grant_read_write_data(ecs_task_role)
        products_table.grant_read_write_data(ecs_task_role)
        
          # Crear una VPC
        vpc = ec2.Vpc(self, "UTNCloudVPC",
            max_azs=2  # Se distribuye en dos zonas de disponibilidad
        )

        # Crear un ECS Cluster
        cluster = ecs.Cluster(self, "AppCluster",
            vpc=vpc
        )

        # Añadir capacidad EC2 al ECS Cluster
        auto_scaling_group = cluster.add_capacity("DefaultAutoScalingGroup",
            instance_type=ec2.InstanceType("t2.micro"),
        )

      

        # Definir una imagen de Docker que será usada por la tarea ECS
        fastapi_task_definition = ecs.Ec2TaskDefinition(self, "FastApiTaskDef",
            task_role=ecs_task_role
        )

        # Usar una imagen 
        fastapi_container = fastapi_task_definition.add_container("FastApiContainer",
            image=ecs.ContainerImage.from_asset(directory="./backend"),
            memory_limit_mib=256,                          
        )

        # Abrir el puerto
        fastapi_container.add_port_mappings(
            ecs.PortMapping(container_port=8000)
        )

        # Crear un servicio ECS para ejecutar la tarea en EC2
        fastapi_ecs_service = ecs.Ec2Service(self, "FastApiService",
            cluster=cluster,
            task_definition=fastapi_task_definition,
           
        )

     

        ##Crear un Security Group que permita la comunicación entre los servicios
        #sg = ec2.SecurityGroup(self, "AppSG", vpc=vpc,
        #    allow_all_outbound=True
        #)

        ## Permitir tráfico entre los servicios dentro de la misma VPC (por ejemplo en puertos 80 y 8000)
        #sg.add_ingress_rule(sg, ec2.Port.tcp(8000), "Allow internal traffic on port 8000")

        # Definir una imagen de Docker que será usada por la tarea ECS
        telegram_task_definition = ecs.Ec2TaskDefinition(self, "TelegramTaskDef")

        # Usar una imagen 
        telegram_container = telegram_task_definition.add_container("TelegramContainer",
            image=ecs.ContainerImage.from_asset(directory= "./go-telegram"),
            memory_limit_mib=256,
            environment={"TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN, "BACKEND_URL": "http://FastApiService.AppCluster.us-west-2.ecs.internal:8000"},                           
        )

        # Abrir el puerto
        telegram_container.add_port_mappings(
            ecs.PortMapping(container_port=80)
        )

        # Crear un servicio ECS para ejecutar la tarea en EC2
        telegram_ecs_service = ecs.Ec2Service(self, "TelegramService",
            cluster=cluster,
            task_definition=telegram_task_definition,
        )




app = App()
AppStack(app, "AppStack")
app.synth()
