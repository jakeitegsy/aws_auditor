import boto3
import os
import datetime
import botocore.exceptions


def region():
    return os.environ.get('AWS_REGION', 'us-east-1')

def endpoint_url(service):
    return
    return f"https://{service}.{region()}.amazonaws.com"

def create_resource(service):
    return session.resource(
        service, endpoint_url=endpoint_url(service)
    )

def create_client(service):
    return session.client(
        service, endpoint_url=endpoint_url(service)
    )

def handler(event, context):
    for bucket in list_buckets():
        table.put_item(
            Item=Bucket(bucket).to_dict()
        )

def list_buckets():
    return (bucket for bucket in s3.list_buckets()['Buckets'])


class Bucket:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.get_bucket_versioning()
        self.encryption = self.get_bucket_encryption()
        self.versioning = self.get_bucket_versioning()

    def getter(self, dictionary, key):
        try:
            return dictionary[key]
        except KeyError:
            return

    def get(self, key):
        return self.getter(self.dictionary, key)

    def get_bucket_attribute(self, getter):
        try:
            return getter(Bucket=self.name())
        except botocore.exceptions.ClientError as error:
            print(f'Cannot get information for {self.name()} because {error}')
            return {}

    def get_bucket_encryption(self):
        try:
            return s3.get_bucket_encryption(Bucket=self.name())['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']
        except Exception:
            return {}

    def get_bucket_versioning(self):
        return self.get_bucket_attribute(s3.get_bucket_versioning)

    def name(self):
        return self.get('Name')

    def created(self):
        return self.get('CreationDate').strftime("%Y-%m-%dT%H:%M:%SZ")

    def get_metric_statistics(self, metric_name=None, storage_type=None, unit=None):
        try:
            return cloudwatch.get_metric_statistics(
                Namespace="AWS/S3",
                MetricName=metric_name,
                Dimensions=[
                    dict(Name="BucketName", Value=self.name()),
                    dict(Name="StorageType", Value=storage_type)
                ],
                StartTime=datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=2),
                EndTime=datetime.datetime.now(datetime.timezone.utc),
                Unit=unit,
                Period=86400,
                Statistics=["Maximum"]
                )["Datapoints"][0].get("Maximum", 0)
        except IndexError:
            return "0"

    def size(self):
        return self.get_metric_statistics(
            metric_name="BucketSizeBytes",
            storage_type="StandardStorage",
            unit="Bytes",
        )

    def size_in_gib(self):
        return float(self.size()) / 1074000000.0

    def number_of_objects(self):
        return self.get_metric_statistics(
            metric_name="NumberOfObjects",
            storage_type="AllStorageTypes",
            unit="Count"
        )

    def versioning_status(self):
        return self.versioning.get('Status')

    def mfa_delete(self):
        return self.versioning.get('MFADelete')

    def encryption_algorithm(self):
        return self.encryption.get('SSEAlgorithm')

    def kms_key_id(self):
        return self.encryption.get("KMSMasterKeyID")

    def to_dict(self):
        return {
            "Name": self.name(),
            "SizeInBytes" : str(self.size()),
            "SizeInGiB" : str(self.size_in_gib()),
            "CreationDate" : self.created(),
            "NumberOfObjects" : str(self.number_of_objects()),
            "Encryption": self.encryption_algorithm(),
            'KmsKeyId': self.kms_key_id(),
            'VersioningStatus': self.versioning_status(),
            'MFADelete': self.mfa_delete(),
            'DateAudited': str(datetime.datetime.now())
        }


session = boto3.session.Session(region_name=region())
s3 = create_client("s3")
cloudwatch = create_client("cloudwatch")
table = boto3.resource('dynamodb').Table(os.environ.get('AUDIT_RECORDS'))