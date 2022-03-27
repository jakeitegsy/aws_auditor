import boto3
import os
import datetime

session = boto3.session.Session(region_name="us-west-2")
table = boto3.resource(
	'dynamodb',
	endpoint_url='https://dynamodb.us-west-2.amazonaws.com'
).Table(os.environ.get('AUDIT_RECORDS'))
lambda_client = session.client('lambda')
paginator = lambda_client.get_paginator('list_functions')


class Function:

	def __init__(self, dictionary):
		self.dictionary = dictionary

	def getter(self, dictionary, key):
		try:
			return dictionary[key]
		except (KeyError, TypeError):
			return

	def get(self, key):
		return self.getter(self.dictionary, key)

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

	def subnet_ids(self):
		return self.get_vpc_config('SubnetIds')

	def security_group_ids(self):
		return self.get_vpc_config('SecurityGroupIds')

	def encryption(self):
		return self.get('KMSKeyArn')

	def to_dict(self):
		return {
	        'Name': self.name(),
			'DateAudited': str(datetime.datetime.now()),
			'Encrytion': self.encryption(),
	        'Role': self.role(),
	        'FunctionArn': self.arn(),
	        'CodeSize': self.code_size(),
	        'MemorySize': self.memory_size(),
	        'Timeout': self.timeout(),
	        'SubnetIds': str(self.subnet_ids()),
	        'SecurityGroupIds': str(self.security_group_ids()),
	        'VpcId': self.vpc_id(),
	    }

def list_functions():
	return [
		function for page in paginator.paginate() for function in page['Functions']
	]

def handler(event, context):
	for function in list_functions():
		table.put_item(Item=Function(function).to_dict())
