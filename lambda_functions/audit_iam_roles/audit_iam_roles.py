import boto3
import os

def region():
    return os.environ.get('AWS_REGION')


class Role:

    def __init__(self, role):
        self.role = role

    def path(self):
        return self.role.get("Path")

    def name(self):
        return self.role.get("RoleName")

    def id(self):
        return self.role.get("RoleId")

    def arn(self):
        return self.role.get("Arn")

    def date_created(self):
        try:
            return self.role["CreateDate"].strftime("%Y-%m-%dT%H:%M:%SZ")
        except KeyError:
            return

    def max_session_duration(self):
        return self.role.get("MaxSessionDuration")

    def to_dict(self):
        return dict(
            Name=self.name(),
            Id=self.id(),
            Arn=self.arn(),
            DateCreated=self.date_created(),
            MaxSessionDuration=self.max_session_duration()
        )

def list_roles():
    return [role for page in PAGINATOR.paginate() for role in page["Roles"]]

def write_to_dynamodb():
    for role in list_roles():
        TABLE.put_item(
            Item=Role(role).to_dict()
        )

def handler(event, context):
    write_to_dynamodb()

session = boto3.session.Session(region_name=region())
IAM = session.client("iam")
PAGINATOR = IAM.get_paginator("list_roles")

TABLE = boto3.resource(
    'dynamodb',
    endpoint_url=f'https://dynamodb.{region()}.amazonaws.com'
).Table(
    os.environ.get('INVENTORY_TABLE_NAME')
)
