from aws_cdk import App

from storage_stack import StorageStack 

from main_stack import MainStack 
        
app = App()

storage_stack = StorageStack(app, "UTNCloudStorageStack")

MainStack(app, "UTNCloudAppStack", storage_stack=storage_stack)

app.synth()
