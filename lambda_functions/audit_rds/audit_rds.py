import boto3
import os
import datetime


class Database(object):

    def __init__(self, database):
        self.database = database

    def get(self, key, default=None):
        return self.database.get(key, default)

    def database_name(self):
        return self.get('DatabaseName')

    def get_availability_zones(self):
        return ", ".join(self.get('AvailabilityZones'))

    def get_security_group_ids(self):
        return ', '.join(security_group['VpcSecurityGroupId'] for security_group in self.get('VpcSecurityGroups'))

    def get_iam_roles(self):
        return ', '.join(role['RoleArn'] for role in self.get('AssociatedRoles'))

    def get_tags(self):
        try:
            return {
                tag['Key']: tag['Value'] for tag in self.get('TagList')
            }
        except (AttributeError, TypeError):
            return {}

    def to_dict(self):
        return {
            'ResourceName': self.database_name(),
            'DateAudited': str(datetime.datetime.now()),
            'ClusterIdentifier': self.get('DBClusterIdentifier'),
            'AvailabilityZones': self.get_availability_zones(),
            'Endpoint': self.get('Endpoint'),
            'MultiAZ': self.get('MultiAZ'),
            'Engine': self.get('Engine'),
            'LastRestorableTime': self.get('LatestRestorableTime'),
            'PreferredBackupWindow': self.get('PreferredBackupWindow'),
            'EncryptedStorage': self.get('StorageEncrypted'),
            'KmsKeyId': self.get('KmsKeyId'),
            'AssociatedIamRoles': self.get_iam_roles(),
            'IAMDatabaseAuthenticationEnabled': self.get('IAMDatabaseAuthenticationEnabled'),
            'DeletionProtection': self.get('DeletionProtection'),
            'DbInstanceClass': self.get('DBClusterInstanceClass'),
            'PerformanceInsightsEnabled': self.get('PerformanceInsightsEnabled'),
            'AutoMinorVersionUpgrade': self.get('AutoMinorVersionUpgrade'),
            'StorageType': self.get('StorageType'),
            'SecurityGroupIds': self.get_security_group_ids(),
            **self.get_tags(),
        }

def region():
    return os.environ.get('REGION')

def get_databases():
    return (
        database for database
        in RDS.describe_db_instances()['DBInstances']
    )

def handler(event, context):
    for database in get_databases():
        TABLE.put_item(Item=Database(database).to_dict())

RDS = boto3.session.Session(region_name=region()).client('rds')
TABLE = boto3.resource(
    'dynamodb',
    endpoint_url=f'https://dynamodb.{region()}.amazonaws.com'
).Table(
    os.environ.get('INVENTORY_TABLE_NAME')
)
