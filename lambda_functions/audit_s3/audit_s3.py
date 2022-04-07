import boto3
import os
import datetime
import botocore.exceptions

class Bucket:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.encryption = self.get_bucket_encryption()
        self.versioning = self.get_bucket_versioning()

    def get_bucket_encryption(self):
        try:
            return S3.get_bucket_encryption(Bucket=self.bucket_name())['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']
        except (IndexError, KeyError):
            return {}

    def bucket_name(self):
        return self.get('Name')

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
                    dict(Name="BucketName", Value=self.bucket_name()),
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
        return float(self.get_size()) / 1074000000.0

    def get_number_of_objects(self):
        return self.get_metric_statistics(
            metric_name="NumberOfObjects",
            storage_type="AllStorageTypes",
            unit="Count"
        )

    def get_bucket_versioning(self):
        return S3.get_bucket_versioning(Bucket=self.bucket_name())

    def get_bucket_location(self):
        return S3.get_bucket_location(Bucket=self.bucket_name())['LocationConstraint']

    def get_tags(self):
        try:
            return {
                tag['Key']: tag['Value']
                for tag in S3.get_bucket_tagging(Bucket=self.bucket_name()).get('TagSet')
            }
        except (KeyError, TypeError):
            return {}

    def to_dict(self):
        return {
            "ResourceName": self.bucket_name(),
            "SizeInBytes" : str(self.get_size()),
            "SizeInGiB" : str(self.get_size_in_gib()),
            "LastModified" : self.get_last_modified_date(),
            "NumberOfObjects" : str(self.get_number_of_objects()),
            "Encryption": self.encryption.get('SSEAlgorithm'),
            'KmsKeyId': self.encryption.get("KMSMasterKeyID"),
            'VersioningStatus': self.versioning.get('Status'),
            'MFADelete': self.versioning.get('MFADelete'),
            'DateAudited': str(datetime.datetime.now()),
            'BucketLocation': self.get_bucket_location(),
            **self.get_tags(),
        }

def now():
    return datetime.datetime.now(datetime.timezone.utc)

def region():
    return os.environ.get('AWS_REGION', 'us-east-1')

def endpoint_url(service):
    return f"https://{service}.{region()}.amazonaws.com"

def create_client(service):
    return SESSION.client(
        service, endpoint_url=endpoint_url(service)
    )

def list_buckets():
    return (bucket for bucket in S3.list_buckets()['Buckets'])

def handler(event, context):
    for bucket in list_buckets():
        TABLE.put_item(
            Item=Bucket(bucket).to_dict()
        )

SESSION = boto3.session.Session(region_name=region())
S3 = create_client("s3")
CLOUDWATCH = create_client("cloudwatch")
TABLE = boto3.resource(
    'dynamodb',
    endpoint_url=f'https://dynamodb.{region()}.amazonaws.com'
).Table(
    os.environ.get('INVENTORY_TABLE_NAME')
)
