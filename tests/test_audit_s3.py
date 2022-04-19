import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import mock_boto3

sys.modules['boto3'] = mock_boto3

import unittest
import lambda_functions.audit_s3.audit_s3 as audit_s3
import datetime


class TestAuditS3(unittest.TestCase):

    def setUp(self):
        self.bucket_info = {
            'Name': 'BucketName',
            'CreationDate': datetime.datetime(2021, 3, 4, 19, 41, tzinfo=datetime.timezone.utc)
        }
        self.tester = audit_s3.Bucket(self.bucket_info)

    def test_bucket_name(self):
        self.assertEqual(self.tester.bucket_name, self.bucket_info['Name'])

    def test_dict(self):
        self.maxDiff = None
        expected = self.tester.to_dict()
        expected.pop('DateAudited')
        self.assertEqual(
            expected,
            {
                'Location': 'region',
                'LastModified': '2021-03-04T19:41:00Z',
                'Encryption': 'aws:kms',
                'KmsKeyId': 'KmsKeyId',
                'MFADelete': 'Disabled',
                'NumberOfObjects': '123.0',
                'ResourceName': 'BucketName',
                'SizeInBytes': '123.0',
                'SizeInGiB': '1.1455267667770386e-07',
                'Versioning': 'Enabled',
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True,
                'EnforceSSL': True,
                'ObjectLockConfiguration': 'Enabled',
                'AccessLogging': True,
                'Key1': 'Value1',
                'Key2': 'Value2',
                'Key3': 'Value3',
                'Key4': 'Value4',
                'LambdaFunctionNotifications': 'LambdaFunctionArn',
                'SQSQueueNotifications': 'QueueArn',
                'SNSTopicNotifications': 'TopicArn',
                'EventBridgeNotifications': '',
            }
        )