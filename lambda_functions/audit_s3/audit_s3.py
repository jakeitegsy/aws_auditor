""" Get an inventory of all s3 buckets with additional attributes to dynamodb table
"""

import boto3
import os
import datetime
import botocore.exceptions
import concurrent.futures
import traceback
import sys


class Bucket:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.bucket_name = self.get('Name')
        self.encryption = self.get_bucket_encryption()
        self.versioning = self.get_bucket_versioning()

    def get_bucket_encryption(self):
        try:
            return S3.get_bucket_encryption(Bucket=self.bucket_name)['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']
        except Exception:
            return {}

    def get(self, key):
        try:
            return self.dictionary[key]
        except KeyError:
            return

    def get_last_modified_date(self):
        return self.get('CreationDate').strftime("%Y-%m-%dT%H:%M:%SZ")

    def get_metric_statistics(self, metric_name=None, storage_type=None, unit=None):
        try:
            return CLOUDWATCH.get_metric_statistics(
                Namespace="AWS/S3",
                MetricName=metric_name,
                Dimensions=[
                    dict(Name="BucketName", Value=self.bucket_name),
                    dict(Name="StorageType", Value=storage_type)
                ],
                StartTime=now() - datetime.timedelta(days=2),
                EndTime=now(),
                Unit=unit,
                Period=86400,
                Statistics=["Maximum"]
            )["Datapoints"][0].get("Maximum", 0)
        except IndexError:
            return "0"

    def get_size(self):
        return self.get_metric_statistics(
            metric_name="BucketSizeBytes",
            storage_type="StandardStorage",
            unit="Bytes",
        )

    def get_size_in_gib(self):
        return float(self.get_size()) / (2 ** 30)

    def get_number_of_objects(self):
        return self.get_metric_statistics(
            metric_name="NumberOfObjects",
            storage_type="AllStorageTypes",
            unit="Count"
        )

    @staticmethod
    def access_denied():
        return 'Access Denied'

    def get_bucket_versioning(self):
        try:
            return S3.get_bucket_versioning(Bucket=self.bucket_name)
        except botocore.exceptions.ClientError:
            return {}

    def get_bucket_location(self):
        try:
            return S3.get_bucket_location(Bucket=self.bucket_name)['LocationConstraint']
        except KeyError:
            return
        except botocore.exceptions.ClientError:
            return self.access_denied()

    def get_object_lock_configuration(self):
        try:
            return S3.get_object_lock_configuration(Bucket=self.bucket_name)['ObjectLockConfiguration']['ObjectLockEnabled']
        except KeyError:
            return 'Disabled'
        except botocore.exceptions.ClientError:
            return self.access_denied()

    def get_enforce_ssl(self):
        try:
            for statement in S3.get_bucket_policy(Bucket=self.bucket_name)['Statement']:
                if statement['Effect'] == 'Deny':
                    if statement['Condition']['Bool']['aws:SecureTransport'] == 'false':
                        return True
        except Exception as error:
            print(f'{self.bucket_name}: get_public_access_configuration raised an error')
            return False

    def get_public_access_configuration(self):
        try:
            return S3.get_public_access_block(Bucket=self.bucket_name).get('PublicAccessBlockConfiguration', {})
        except Exception as error:
            print(f'{self.bucket_name}: get_public_access_configuration raised an error')
            return {
                key: False for key in (
                    'BlockPublicAcls', 'BlockPublicPolicy',
                    'IgnorePublicAcls', 'RestrictPublicBuckets'
                )
            }

    def get_bucket_logging(self):
        try:
            return 'LoggingEnabled' in S3.get_bucket_logging(Bucket=self.bucket_name)
        except botocore.exceptions.ClientError:
            return

    def get_bucket_notification_configuration(self):
        result = {
            'LambdaFunctionNotifications': None,
            'SQSQueueNotifications': None,
            'SNSTopicNotifications': None,
            'EventBridgeNotifications': None,
        }
        try:
            for key, configuration in S3.get_bucket_notification_configuration(Bucket=self.bucket_name).items():
                if key == 'TopicConfigurations':
                    result['SNSTopicNotifications'] = ','.join(topic['TopicArn'] for topic in configuration)
                if key == 'LambdaFunctionConfigurations':
                    result['LambdaFunctionNotifications'] = ','.join(function['LambdaFunctionArn'] for function in configuration)
                if key == 'QueueConfigurations':
                    result['SQSQueueNotifications'] = ','.join(queue['QueueArn'] for queue in configuration)
                if key == 'EventBridgeConfiguration':
                    result['EventBridgeNotifications'] = ','.join(event['EventBridgeArn'] for event in configuration)
        except Exception as error:
            print(f'{self.bucket_name}: get_bucket_notification_configuration raised an error')
        return result

    def get_tags(self):
        try:
            return {
                tag['Key']: tag['Value']
                for tag in S3.get_bucket_tagging(Bucket=self.bucket_name).get('TagSet')
            }
        except Exception:
            return {}

    def to_dict(self):
        return {
            "ResourceName": self.bucket_name,
            "SizeInBytes" : str(self.get_size()),
            "SizeInGiB" : str(self.get_size_in_gib()),
            "LastModified" : self.get_last_modified_date(),
            "NumberOfObjects" : str(self.get_number_of_objects()),
            "Encryption": self.encryption.get('SSEAlgorithm'),
            'KmsKeyId': self.encryption.get("KMSMasterKeyID"),
            'Versioning': self.versioning.get('Status'),
            'MFADelete': self.versioning.get('MFADelete'),
            'DateAudited': str(datetime.datetime.now()),
            'Location': self.get_bucket_location(),
            'EnforceSSL': self.get_enforce_ssl(),
            'ObjectLockConfiguration': self.get_object_lock_configuration(),
            'AccessLogging': self.get_bucket_logging(),
            **self.get_bucket_notification_configuration(),
            **self.get_public_access_configuration(),
            **self.get_tags(),
        }

def now():
    return datetime.datetime.now(datetime.timezone.utc)

def region():
    return os.environ.get('AWS_REGION', 'us-east-1')

def list_buckets():
    return (bucket for bucket in S3.list_buckets()['Buckets'])

def handler(event, context):
    for bucket in list_buckets():
        TABLE.put_item(
            Item=Bucket(bucket).to_dict()
        )


SESSION = boto3.session.Session(region_name=region())
S3 = boto3.client("s3")
CLOUDWATCH = boto3.client("cloudwatch")
TABLE = boto3.resource(
    'dynamodb',
    endpoint_url=f'https://dynamodb.{region()}.amazonaws.com'
).Table(
    os.environ.get('INVENTORY_TABLE_NAME')
)