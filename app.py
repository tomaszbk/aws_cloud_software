from aws_cdk import (
    App,
    Stack,
    aws_lambda as _lambda,
    aws_ec2 as ec2,
    aws_ecs as ecs,
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

        #email_lambda = _lambda.DockerImageFunction(
        #    self,
        #    "EmailLambda",
        #    code=_lambda.DockerImageCode.from_image_asset("./email_lambda"),
        #    environment={"SENDER_EMAIL": SENDER_EMAIL, "SENDER_PASSWORD": SENDER_PASSWORD},
        #)

        
          # Crear una VPC
        vpc = ec2.Vpc(self, "MyVpc",
            max_azs=2  # Se distribuye en dos zonas de disponibilidad
        )

        # Crear un ECS Cluster
        cluster = ecs.Cluster(self, "MyEcsCluster",
            vpc=vpc
        )

        # Añadir capacidad EC2 al ECS Cluster
        auto_scaling_group = cluster.add_capacity("DefaultAutoScalingGroup",
            instance_type=ec2.InstanceType("t2.micro"),
        )

        # Definir una imagen de Docker que será usada por la tarea ECS
        task_definition_telegram = ecs.Ec2TaskDefinition(self, "TaskDef")

        # Usar una imagen 
        container_telegram = task_definition_telegram.add_container("WebContainer",
            image=ecs.ContainerImage.from_asset("./go-telegram"),
            memory_limit_mib=256,
            environment={"TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN}                           
        )

        # Abrir el puerto 80 para permitir tráfico web
        container_telegram.add_port_mappings(
            ecs.PortMapping(container_port=80)
        )

        # Crear un servicio ECS para ejecutar la tarea en EC2
        ecs_service = ecs.Ec2Service(self, "MyEc2Service",
            cluster=cluster,
            task_definition=task_definition_telegram
        )




app = App()
AppStack(app, "AppStack")
app.synth()
