import os

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_servicediscovery as servicediscovery,
)
from constructs import Construct
from dotenv import load_dotenv

from storage_stack import StorageStack

load_dotenv()

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
AWS_BEDROCK_MODEL = os.environ.get("AWS_BEDROCK_MODEL")
AWS_BEDROCK_REGION = os.environ.get("AWS_BEDROCK_REGION")
DEBUG = os.environ.get("DEBUG")


class VpcEcsStack(Stack):
    def __init__(self, scope: Construct, id: str, storage_stack: StorageStack, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Crear una VPC
        vpc = ec2.Vpc(
            self,
            "UTNCloudVPC",
            max_azs=2,  # Se distribuye en dos zonas de disponibilidad
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                )
            ],
            enable_dns_support=True,
            enable_dns_hostnames=True,
        )

        namespace = servicediscovery.PrivateDnsNamespace(
            self, "UtnCloudNamespace", name="utn-shop.namespace", vpc=vpc
        )

        security_group = ec2.SecurityGroup(
            self,
            "EcsSecurityGroup",
            vpc=vpc,
            description="Allow outbound traffic",
            allow_all_outbound=True,  # Allow all outbound traffic
        )

        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),  # Allow traffic from any IPv4 address
            connection=ec2.Port.tcp(80),  # Allow traffic on port 80 (HTTP)
            description="Allow HTTP traffic from the internet",
        )

        # Add inbound rule for HTTPS
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),  # Allow traffic from  from the internet
            connection=ec2.Port.tcp(443),  # Allow TCP traffic on port 443
            description="Allow HTTPS traffic from the internet",
        )

        # Add inbound rule for HTTPS
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(8000),  # Allow TCP traffic on port 8000
            description="Allow traffic from the internet",
        )

        # Crear un ECS Cluster
        cluster = ecs.Cluster(self, "AppCluster", cluster_name="UtnCloudECS_Cluster", vpc=vpc)

        # Create an IAM Role for ECS Task Definition
        ecs_task_role = iam.Role(
            self, "ECSTaskRole", assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )

        storage_stack.image_bucket.grant_read_write(ecs_task_role)
        storage_stack.users_table.grant_read_write_data(ecs_task_role)
        storage_stack.products_table.grant_read_write_data(ecs_task_role)

        ecs_task_role.add_to_policy(
            iam.PolicyStatement(actions=["events:PutEvents"], resources=["*"])
        )
        # Attach Bedrock permissions to the role
        ecs_task_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock:InvokeModel",  # Action to invoke a model in Bedrock
                    "bedrock:ListModels",  # Action to list available models
                    "bedrock:GetModel",  # Action to get details of a specific model
                    # Add any other necessary Bedrock permissions here
                ],
                resources=["*"],  # Ideally, restrict this to specific Bedrock resources
            )
        )

        # Definir una imagen de Docker que será usada por la tarea ECS
        fastapi_task_definition = ecs.FargateTaskDefinition(
            self, "FastApiTaskDef", task_role=ecs_task_role
        )
        # Usar una imagen
        fastapi_container = fastapi_task_definition.add_container(
            "FastApiContainer",
            image=ecs.ContainerImage.from_asset(directory="./backend"),
            container_name="FastApiContainer",
            logging=ecs.LogDrivers.aws_logs(stream_prefix="fastapi-backend"),
            memory_limit_mib=256,
            environment={
                "DEBUG": DEBUG,
                "AWS_BEDROCK_MODEL": AWS_BEDROCK_MODEL,
                "AWS_BEDROCK_REGION": AWS_BEDROCK_REGION,
            },
        )

        # Abrir el puerto
        fastapi_container.add_port_mappings(ecs.PortMapping(container_port=8000))

        # Crear un servicio ECS para ejecutar la tarea en EC2
        fastapi_ecs_service = ecs.FargateService(
            self,
            "FastApiService",
            service_name="fastapiservice",
            cluster=cluster,
            task_definition=fastapi_task_definition,
            security_groups=[security_group],
            assign_public_ip=True,
            cloud_map_options=ecs.CloudMapOptions(
                name="backend-service", cloud_map_namespace=namespace
            ),
        )

        # Definir una imagen de Docker que será usada por la tarea ECS
        telegram_task_definition = ecs.FargateTaskDefinition(self, "TelegramTaskDef")

        # Usar una imagen
        telegram_container = telegram_task_definition.add_container(
            "TelegramContainer",
            image=ecs.ContainerImage.from_asset(directory="./go-telegram"),
            container_name="TelegramContainer",
            memory_limit_mib=256,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="telegram"),
            environment={
                "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
                "BACKEND_HOST": "backend-service.utn-shop.namespace",
                "BACKEND_PORT": "8000",
            },
        )

        # Abrir el puerto
        telegram_container.add_port_mappings(
            ecs.PortMapping(container_port=80),
            ecs.PortMapping(container_port=443),
        )

        # Crear un servicio ECS para ejecutar la tarea en EC2
        telegram_ecs_service = ecs.FargateService(
            self,
            "TelegramService",
            service_name="telegramservice",
            cluster=cluster,
            task_definition=telegram_task_definition,
            security_groups=[security_group],
            assign_public_ip=True,
            cloud_map_options=ecs.CloudMapOptions(name="telegram-service", cloud_map_namespace=namespace),
        )

        telegram_ecs_service.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Allow inbound HTTP traffic"
        )
        telegram_ecs_service.connections.allow_from_any_ipv4(
            ec2.Port.tcp(443), "Allow inbound HTTPs traffic"
        )
