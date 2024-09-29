from aws_cdk import (
    App,
    Stack,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_s3 as s3,
    aws_dynamodb as ddb,
    aws_iam as iam,
    aws_autoscaling as autoscaling,
    aws_events as events,
    aws_events_targets as events_targets,
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

        #image_bucket = s3.Bucket(self, "ProductImages", 
        #    bucket_name="product-images-utn-frlp", 
        #    removal_policy=RemovalPolicy.DESTROY)

        #products_table = ddb.Table(
        #    self, 'ProductsTable',
        #    table_name='products',
        #    partition_key={'name': 'category', 'type': ddb.AttributeType.STRING},
        #    sort_key={'name': 'product_id', 'type': ddb.AttributeType.NUMBER},
        #    removal_policy=RemovalPolicy.DESTROY
        #)
        #
        #users_table = ddb.Table(
        #    self, 'UsersTable',
        #    table_name='users',
        #    partition_key={'name': 'phone_number', 'type': ddb.AttributeType.STRING},
        #    removal_policy=RemovalPolicy.DESTROY
        #)
        # Create an IAM Role for ECS Task Definition
        ecs_task_role = iam.Role(self, "ECSTaskRole",
           assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )

        # image_bucket.grant_read_write(ecs_task_role)
        # users_table.grant_read_write_data(ecs_task_role)
        # products_table.grant_read_write_data(ecs_task_role)
        
          # Crear una VPC
        vpc = ec2.Vpc(self, "UTNCloudVPC",
            max_azs=2, # Se distribuye en dos zonas de disponibilidad
            nat_gateways=0,
        )

    
        security_group = ec2.SecurityGroup(self, "EcsSecurityGroup",
        vpc=vpc,
        description="Allow HTTP traffic",
        allow_all_outbound=True  # Allow all outbound traffic
        )
        
        security_group.add_ingress_rule(
        peer=ec2.Peer.any_ipv4(),  # Allow traffic from any IPv4 address
        connection=ec2.Port.tcp(80),  # Allow traffic on port 80 (HTTP)
        description="Allow HTTP traffic from the internet"
        )


        # Crear un ECS Cluster
        cluster = ecs.Cluster(self, "AppCluster",
            cluster_name="appcluster098098098095",
            vpc=vpc
        )

        # Añadir capacidad EC2 al ECS Cluster
        auto_scaling_group = autoscaling.AutoScalingGroup(self, "ASG",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ecs.EcsOptimizedImage.amazon_linux2(),  # ECS-optimized AMI
            associate_public_ip_address=True,  # Asignar IP pública a las instancias
            min_capacity=1,  # Minimum number of EC2 instances
            max_capacity=10   # Maximum number of EC2 instances to scale
        )

        capacity_provider = ecs.AsgCapacityProvider(self, "CapacityProvider",
            auto_scaling_group=auto_scaling_group,
            enable_managed_termination_protection=False
        )
      
        cluster.add_asg_capacity_provider(capacity_provider)

        

        # Definir una imagen de Docker que será usada por la tarea ECS
        fastapi_task_definition = ecs.Ec2TaskDefinition(self, "FastApiTaskDef",
           task_role=ecs_task_role
        )

        # Usar una imagen 
        fastapi_container = fastapi_task_definition.add_container("FastApiContainer",
           image=ecs.ContainerImage.from_asset(directory="./backend"),
           container_name="FastApiContainer7349874289",
           memory_limit_mib=256,                          
        )

        # Abrir el puerto
        fastapi_container.add_port_mappings(
           ecs.PortMapping(container_port=8000)
        )

        # Crear un servicio ECS para ejecutar la tarea en EC2
        fastapi_ecs_service = ecs.Ec2Service(self, "FastApiService",
           service_name= 'fastapiservice78987987',
           cluster=cluster,
           task_definition=fastapi_task_definition,
          
        )


        # Definir una imagen de Docker que será usada por la tarea ECS
        telegram_task_definition = ecs.Ec2TaskDefinition(self, "TelegramTaskDef",
            network_mode=ecs.NetworkMode.AWS_VPC,)

        # Usar una imagen 
        telegram_container = telegram_task_definition.add_container("TelegramContainer",
            image=ecs.ContainerImage.from_asset(directory= "./go-telegram"),
            container_name="TelegramContainer7349874289",
            memory_limit_mib=256,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="telegram"),
            environment={"TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN, 
                         "BACKEND_HOST": 'http://fastapiservice78987987.appcluster098098098095.us-west-2.ecs.internal',
                         "BACKEND_PORT": '8000'},                           
        )

        # Abrir el puerto
        telegram_container.add_port_mappings(
            ecs.PortMapping(container_port=80)
        )

        # Crear un servicio ECS para ejecutar la tarea en EC2
        telegram_ecs_service = ecs.Ec2Service(self, "TelegramService",
            service_name= 'telegramservice78987987',
            cluster=cluster,
            task_definition=telegram_task_definition,
            security_groups=[security_group],  
            vpc_subnets= ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        
        )

        event_rule = events.Rule(
            self, "MyEventRule",
            event_pattern={
                "source": ["my.application"],
                "detail-type": ["MyAppEvent"],
            }
        )

        # Add the Lambda function as a target to the EventBridge rule
        event_rule.add_target(events_targets.LambdaFunction(email_lambda))

        ecs_task_role.add_to_policy(iam.PolicyStatement(
            actions=["events:PutEvents"],
            resources=["*"]
        ))

        # Attach Bedrock permissions to the role
        ecs_task_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "bedrock:InvokeModel",          # Action to invoke a model in Bedrock
                "bedrock:ListModels",           # Action to list available models
                "bedrock:GetModel",             # Action to get details of a specific model
                # Add any other necessary Bedrock permissions here
            ],
            resources=["*"]  # Ideally, restrict this to specific Bedrock resources
        ))




app = App()
AppStack(app, "AppStack")
app.synth()
