
# Welcome to the AWS Auditor Project

This is a collection of Lambda Functions to Audit AWS Resources.

## Components
- AWS Lambda Function
- DynamoDB Table

## Auditors
- audit_lambda
- audit_iam_roles
- audit_s3
- audit_dynamodb
- audit_rds
- audit_ec2
- audit_ebs
- audit_workspaces
- audit_cloudwatch_logs
- audit_cloudwatch_alarms
- audit_sns_topics

### How to activate the virtual environment
```
source .venv/bin/activate
```
### How to list all stacks
```
cdk ls
```

### How to view all stacks
```
cdk synth --all
```

### How to install Requirements
```
pip install -r requirements.txt
```