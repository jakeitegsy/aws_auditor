import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import mock_boto3

sys.modules['boto3'] = mock_boto3
os.environ['INVENTORY_TABLE_NAME'] = 'audit-lambda'
import unittest
import lambda_functions.audit_lambda.audit_lambda


class TestAuditLambda(unittest.TestCase):

    def setUp(self):
        self.function_name = 'function_name'
        self.configuration = {
            'FunctionName': self.function_name,
            'FunctionArn': f'arn:aws:lambda:REGION:123456789012:function:{self.function_name}',
            'Runtime': 'python3.7',
            'Role': f'arn:aws:iam::123456789012:role/{self.function_name}',
            'Handler': f'{self.function_name}.handler',
            'CodeSize': 1234,
            'Description': 'Description',
            'Timeout': 123,
            'MemorySize': 123,
            'LastModified': '1900-12-12T12:59:59.657+0000',
            'CodeSha256': 'ABCabCaa0bAbCABcABCaBc1ABcABcaBCA01ABCaBcAB=',
            'Version': '$LATEST',
            'VpcConfig': {
                'SubnetIds': [
                    'subnet-01234ab0c56d7890d',
                    'subnet-01234ab0c56d7890d',
                    'subnet-01234ab0c56d7890d',
                    'subnet-01234ab0c56d7890d',
                ],
                'SecurityGroupIds': [
                    'sg-012a34b56def78901',
                    'sg-012a34b56def78901',
                    'sg-012a34b56def78901',
                    'sg-012a34b56def78901',
                ],
                'VpcId': 'vpc-1a23456a123a456bd'
            },
            'TracingConfig': {'Mode': 'PassThrough'},
            'RevisionId': 'fba95d87-de7b-4a20-99d1-5fe4780acdc7',
            'KMSKeyArn': 'arn:aws:kms:REGION:123456789012:key/12ab3456-c789-0123-45d6-78e9f0a12bcd'
        }
        self.details = {
            "ResponseMetadata": None,
            "Configuration": {
                "FunctionName": self.function_name,
                "FunctionArn": f"arn:aws:lambda:REGION:123456789012:function:{self.function_name}",
                "Runtime": "python3.8",
                "Role": f'arn:aws:iam::123456789012:role/{self.function_name}',
                "Handler": f'{self.function_name}.handler',
                "CodeSize": 1234,
                "Description": 'Description',
                "Timeout": 123,
                "MemorySize": 123,
                "LastModified": '1900-12-12T12:59:59.657+0000',
                "CodeSha256": 'ABCabCaa0bAbCABcABCaBc1ABcABcaBCA01ABCaBcAB=',
                "Version": "$LATEST",
                "TracingConfig": {
                    "Mode": "PassThrough"
                },
                "RevisionId": 'fba95d87-de7b-4a20-99d1-5fe4780acdc7',
                "State": "Active",
                "LastUpdateStatus": "Successful",
                "PackageType": "Zip",
                "Architectures": [
                    "x86_64"
                ]
            },
            "Code": {
                "RepositoryType": "S3",
                "Location": 'url'
            },
            "Tags": {
                "key1": "value1",
                "key2": "value2",
                "key3": "value3",
                "keyN": "valueN",
            }
        }
        self.function = lambda_functions.audit_lambda.audit_lambda.Function(
            configuration=self.configuration,
            # details=self.details,
        )

    def no_vpc_fixture(self):
        return {
            'FunctionName': self.function_name,
            'FunctionArn': f'arn:aws:lambda:REGION:123456789012:function:{self.function_name}',
            'Runtime': 'python3.7',
            'Role': f'arn:aws:iam::123456789012:role/{self.function_name}',
            'Handler': f'{self.function_name}.handler',
            'CodeSize': 1234,
            'Description': 'Description',
            'Timeout': 123,
            'MemorySize': 123,
            'LastModified': '1900-12-12T12:59:59.657+0000',
            'CodeSha256': 'ABCabCaa0bAbCABcABCaBc1ABcABcaBCA01ABCaBcAB=',
            'Version': '$LATEST',
            'VpcConfig': {
                'SubnetIds': [
                    'subnet-01234ab0c56d7890d', 'subnet-01234ab0c56d7890d'
                ],
                'SecurityGroupIds': [
                    'sg-012a34b56def78901', 'sg-012a34b56def78901'
                ],
                'VpcId': 'vpc-1a23456a123a456bd'
            },
            'TracingConfig': {'Mode': 'PassThrough'},
            'RevisionId': 'fba95d87-de7b-4a20-99d1-5fe4780acdc7',
            'KMSKeyArn': 'arn:aws:kms:REGION:123456789012:key/12ab3456-c789-0123-45d6-78e9f0a12bcd'
        }

    def test_name(self):
        self.assertEqual(self.function.name(), self.configuration['FunctionName'])

    def test_function_arn(self):
        self.assertEqual(self.function.arn(), self.configuration['FunctionArn'])

    def test_runtime(self):
        self.assertEqual(self.function.runtime(), self.configuration['Runtime'])

    def test_role(self):
        self.assertEqual(self.function.role(), self.configuration['Role'])

    def test_code_size(self):
        self.assertEqual(
            self.function.code_size(), self.configuration['CodeSize']
        )

    def test_encryption(self):
        self.assertEqual(
            self.function.encryption(),
            self.configuration['KMSKeyArn']
        )

    def test_description(self):
        self.assertEqual(
            self.function.description(), self.configuration['Description']
        )

    def test_memory_size(self):
        self.assertEqual(
            self.function.memory_size(),
            self.configuration['MemorySize']
        )

    def test_timeout(self):
        self.assertEqual(self.function.timeout(), self.configuration['Timeout'])

    def test_vpc_id(self):
        self.assertEqual(
            self.function.vpc_id(),
            self.configuration['VpcConfig']['VpcId']
        )

    def test_subnet_ids(self):
        self.assertEqual(
            self.function.get_subnet_ids(),
            {
                'SubnetId0': 'subnet-01234ab0c56d7890d',
                'SubnetId1': 'subnet-01234ab0c56d7890d',
                'SubnetId2': 'subnet-01234ab0c56d7890d',
                'SubnetId3': 'subnet-01234ab0c56d7890d',
            }
        )

    def test_security_group_ids(self):
        self.assertEqual(
            self.function.get_security_group_ids(),
            {
                'SecurityGroupId0': 'sg-012a34b56def78901',
                'SecurityGroupId1': 'sg-012a34b56def78901',
                'SecurityGroupId2': 'sg-012a34b56def78901',
                'SecurityGroupId3': 'sg-012a34b56def78901',
            }
        )

    def test_code_location(self):
        self.assertEqual(
            self.function.get_code_location(),
            self.details['Code']['Location']
        )

    def test_tags(self):
        self.assertEqual(
            self.function.get_tags(),
            self.details['Tags']
        )

    def test_dictionary(self):
        self.maxDiff = None
        actual = self.function.to_dict()
        actual.pop('DateAudited')
        self.assertEqual(
            actual,
            {
                'CodeLocation': 'url',
                'CodeSize': 1234,
                'Encrytion': 'arn:aws:kms:REGION:123456789012:key/12ab3456-c789-0123-45d6-78e9f0a12bcd',
                'FunctionArn': 'arn:aws:lambda:REGION:123456789012:function:function_name',
                'MemorySize': 123,
                'ResourceName': 'function_name',
                'Role': 'arn:aws:iam::123456789012:role/function_name',
                'Runtime': 'python3.7',
                'SecurityGroupId0': 'sg-012a34b56def78901',
                'SecurityGroupId1': 'sg-012a34b56def78901',
                'SecurityGroupId2': 'sg-012a34b56def78901',
                'SecurityGroupId3': 'sg-012a34b56def78901',
                'SubnetId0': 'subnet-01234ab0c56d7890d',
                'SubnetId1': 'subnet-01234ab0c56d7890d',
                'SubnetId2': 'subnet-01234ab0c56d7890d',
                'SubnetId3': 'subnet-01234ab0c56d7890d',
                'Timeout': 123,
                'VpcId': 'vpc-1a23456a123a456bd',
                'key1': 'value1',
                'key2': 'value2',
                'key3': 'value3',
                'keyN': 'valueN'
            }
        )