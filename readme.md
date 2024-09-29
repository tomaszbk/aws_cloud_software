# AWS Cloud Software Project

## Project Description
This project involves a microservice application which includes a telegram bot, which connects the user to a llm model that can access a database and provide information to the user. The project is deployed on AWS.

<img src="docs/diagram.png" alt="Image Description" width="800">


## UV Instructions

To install venv with optional de vdependencies:
```bash
uv sync --extra dev
```

To add a dev dependency:
```bash
uv add <package> --optional dev
```

# CDK Instructions

To deploy the project: command:
```bash
cdk deploy
```