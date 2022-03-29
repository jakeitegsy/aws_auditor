import unittest
import os
os.environ['INVENTORY_TABLE_NAME'] = 'audit-lambda'
from lambda_functions.audit_lambda.audit_lambda import Function


class TestAuditLambda(unittest.TestCase):

    def setUp(self):
        self.function_name = 'function_name'
        self.function = Function(
            configuration=self.lambda_function(),
            details=self.function_details(),
        )


    def lambda_function(self):
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

    def function_details(self):
        return {
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

    def test_name(self):
        self.assertEqual(self.function.name(), self.lambda_function()['FunctionName'])

    def test_function_arn(self):
        self.assertEqual(self.function.arn(), self.lambda_function()['FunctionArn'])

    def test_runtime(self):
        self.assertEqual(self.function.runtime(), self.lambda_function()['Runtime'])

    def test_role(self):
        self.assertEqual(self.function.role(), self.lambda_function()['Role'])

    def test_code_size(self):
        self.assertEqual(
            self.function.code_size(), self.lambda_function()['CodeSize']
        )

    def test_encryption(self):
        self.assertEqual(
            self.function.encryption(),
            self.lambda_function()['KMSKeyArn']
        )

    def test_description(self):
        self.assertEqual(
            self.function.description(), self.lambda_function()['Description']
        )

    def test_memory_size(self):
        self.assertEqual(
            self.function.memory_size(),
            self.lambda_function()['MemorySize']
        )

    def test_timeout(self):
        self.assertEqual(self.function.timeout(), self.lambda_function()['Timeout'])

    def test_vpc_id(self):
        self.assertEqual(
            self.function.vpc_id(),
            self.lambda_function()['VpcConfig']['VpcId']
        )

    def test_subnet_ids(self):
        self.assertEqual(
            self.function.subnet_ids(),
            self.lambda_function()['VpcConfig']['SubnetIds']
        )

    def test_security_group_ids(self):
        self.assertEqual(
            self.function.security_group_ids(),
            self.lambda_function()['VpcConfig']['SecurityGroupIds']
        )

    def test_code_location(self):
        self.assertEqual(
            self.function.get_code_location(),
            self.function_details()['Code']['Location']
        )

    def test_tags(self):
        self.assertEqual(
            self.function.get_tags(),
            self.function_details()['Tags']
        )

    @unittest.expectedFailure
    def test_dictionary(self):
        self.maxDiff = None
        self.assertEqual(
            self.function.to_dict(),
            {
                'Code': 'url',
                'CodeSize': 1234,
                'DateAudited': '2022-03-29 08:28:43.517543',
                'Encrytion': 'arn:aws:kms:REGION:123456789012:key/12ab3456-c789-0123-45d6-78e9f0a12bcd',
                'FunctionArn': 'arn:aws:lambda:REGION:123456789012:function:function_name',
                'MemorySize': 123,
                'ResourceName': 'function_name',
                'Role': 'arn:aws:iam::123456789012:role/function_name',
                'Runtime': 'python3.7',
                'SecurityGroupIds': "['sg-012a34b56def78901', 'sg-012a34b56def78901']",
                'SubnetIds': "['subnet-01234ab0c56d7890d', 'subnet-01234ab0c56d7890d']",
                'Timeout': 123,
                'VpcId': 'vpc-1a23456a123a456bd',
                'key1': 'value1',
                'key2': 'value2',
                'key3': 'value3',
                'keyN': 'valueN'
            }

        )