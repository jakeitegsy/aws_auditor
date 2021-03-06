""" Get an inventory of all Lambda Functions in the account
    Writes inventory to dynamodb table
"""

import boto3
import os
import datetime
import concurrent.futures
import sys
import traceback

class Function:

    def __init__(self, configuration):
        self.configuration = configuration
        self.details = self.get_details()

    def get_details(self):
        return LAMBDA.get_function(FunctionName=self.name())

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
        try:
            return {
                f'SubnetId{number}': subnet_ids[number]
                for number in range(len(subnet_ids))
            }
        except (AttributeError, TypeError):
            return {}

    def get_security_group_ids(self):
        security_group_ids = self.get_vpc_config('SecurityGroupIds')
        try:
            return {
                f'SecurityGroupId{number}': security_group_ids[number]
                for number in range(len(security_group_ids))
            }
        except (AttributeError, TypeError):
            return {}

    def encryption(self):
        return self.configuration.get('KMSKeyArn', 'aws:lambda')

    def get_tags(self):
        try:
            return {
                key: value for key, value in self.details.get('Tags').items()
            }
        except (AttributeError, TypeError):
            return {}

    def get_code_location(self):
        return self.details['Code']['Location']

    def to_dict(self):
        return {
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
            **self.get_security_group_ids(),
            **self.get_subnet_ids(),
            **self.get_tags(),
        }

def region():
    return os.environ.get('REGION')

def list_functions():
    return [
        lambda_function for page in PAGINATED_LIST_OF_FUNCTIONS.paginate()
        for lambda_function in page['Functions']
    ]

def handler(event, context):
    for lambda_function in list_functions():
        TABLE.put_item(
            Item=Function(lambda_function).to_dict()
        )


LAMBDA = boto3.session.Session(region_name=region()).client('lambda')
PAGINATED_LIST_OF_FUNCTIONS = LAMBDA.get_paginator('list_functions')
TABLE = boto3.resource(
    'dynamodb',
    endpoint_url=f'https://dynamodb.{region()}.amazonaws.com'
).Table(
    os.environ.get('INVENTORY_TABLE_NAME')
)
