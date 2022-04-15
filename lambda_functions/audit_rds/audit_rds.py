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
        result = []
        for security_group in self.get('VpcSecurityGroups'):
            result.append(security_group['VpcSecurityGroupId'])
        return {}

    def get_iam_roles(self):
        result = []
        for role in self.get('AssociatedRoles'):
            result.append(role['RoleArn'])
        return result

    def get_tags(self):
        try:
            return {
                key: value for key, value in self.get('TagList')
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
            **self.get_security_group_ids(),
            **self.get_tags(),
        }

def region():
    return os.environ.get('REGION')

def list_of_databases():
    return (
        database for database
        in RDS.describe_db_clusters()['DBClusters']
    )




RDS = boto3.session.Session(region_name=region()).client('rds')
TABLE = boto3.resource(
    'dynamodb',
    endpoint_url=f'https://dynamodb.{region()}.amazonaws.com'
).Table(
    os.environ.get('INVENTORY_TABLE_NAME')
)
