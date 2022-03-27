import boto3

session = boto3.session.Session(region_name="us-west-2")
iam = session.client("iam")
paginator = iam.get_paginator("list_roles")
dynamodb = session.resource('dynamodb', endpoint_url='https://dynamodb.us-west-2.amazonaws.com')


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
    return [role for page in paginator.paginate() for role in page["Roles"]]

def write_to_dynamodb():
    table = dynamodb.Table("cdm_audit_iam_roles")
    with table.batch_writer() as batch:
        for role in list_roles():
            batch.put_item(Item=Role(role).to_dict())

def handler(event, context):
    write_to_dynamodb()
