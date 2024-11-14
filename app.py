from aws_cdk import App

from stacks.storage_stack import StorageStack 

from stacks.main_stack import MainStack 

from stacks.vpc_ecs_stack import VpcEcsStack
        
app = App()

storage_stack = StorageStack(app, "UTNCloudStorageStack")

MainStack(app, "UTNCloudAppStack", storage_stack=storage_stack)

VpcEcsStack(app, "UTNCloudVpcEcsStack", storage_stack=storage_stack)

app.synth()
