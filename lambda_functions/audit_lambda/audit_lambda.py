import boto3
import os
import datetime

class Function:

    def __init__(self, configuration=None, details=None):
        self.configuration = configuration
        self.details = details

    def getter(self, dictionary, key):
        try:
            return dictionary[key]
        except (KeyError, TypeError):
            return

    def get(self, key):
        return self.getter(self.configuration, key)

    def get_vpc_config(self, key):
        return self.getter(self.get('VpcConfig'), key)

    def vpc_config(self):
        return self.get('VpcConfig')

    def name(self):
        return self.get('FunctionName')

    def arn(self):
        return self.get('FunctionArn')

    def runtime(self):
        return self.get('Runtime')

    def role(self):
        return self.get('Role')

    def code_size(self):
        return self.get('CodeSize')

    def description(self):
        return self.get('Description')

    def timeout(self):
        return self.get('Timeout')

    def memory_size(self):
        return self.get('MemorySize')

    def vpc_id(self):
        return self.get_vpc_config('VpcId')

    def get_subnet_ids(self):
        subnet_ids = self.get_vpc_config('SubnetIds')
        return {
            f'SubnetId{number}': subnet_ids[number]
            for number in range(len(subnet_ids))
        }

    def get_security_group_ids(self):
        security_group_ids = self.get_vpc_config('SecurityGroupIds')
        return {
            f'SecurityGroupId{number}': security_group_ids[number]
            for number in range(len(security_group_ids))
        }

    def encryption(self):
        return self.configuration.get('KMSKeyArn', 'aws:lambda')

    def get_tags(self):
        tags =  self.details.get('Tags')
        result = {}
        for key, value in tags.items():
            result.update({key: value})
        return result

    def get_code_location(self):
        return self.details['Code']['Location']

    def to_dict(self):
        result = {
            'ResourceName': self.name(),
            'DateAudited': str(datetime.datetime.now()),
            'Encrytion': self.encryption(),
            'Role': self.role(),
            'FunctionArn': self.arn(),
            'CodeSize': self.code_size(),
            'MemorySize': self.memory_size(),
            'Runtime': self.runtime(),
            'Timeout': self.timeout(),
            'VpcId': self.vpc_id(),
            'CodeLocation': self.get_code_location(),
        }
        for dictionary in (
            self.get_security_group_ids(),
            self.get_subnet_ids(),
            self.get_tags(),
        ):
            result.update(dictionary)
        return result

def region():
    return os.environ.get('AWS_REGION')
def list_functions():
    return [
        lambda_function for page in PAGINATED_LIST_OF_FUNCTIONS.paginate()
        for lambda_function in page['Functions']
    ]

def handler(event, context):
    for lambda_function in list_functions():
        TABLE.put_item(
            Item=Function(
                configuration=lambda_function,
                details=lambda_client.get_function(lambda_function)
            ).to_dict()
        )

session = boto3.session.Session(region_name=region())
lambda_client = session.client('lambda')

PAGINATED_LIST_OF_FUNCTIONS = lambda_client.get_paginator('list_functions')
TABLE = boto3.resource(
    'dynamodb',
    endpoint_url=f'https://dynamodb.{region()}.amazonaws.com'
).Table(
    os.environ.get('INVENTORY_TABLE_NAME')
)
