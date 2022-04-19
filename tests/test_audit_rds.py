import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import mock_boto3

sys.modules['boto3'] = mock_boto3
os.environ['INVENTORY_TABLE_NAME'] = 'audit-lambda'

import unittest
import datetime
import lambda_functions.audit_rds.audit_rds


class TestAuditRds(unittest.TestCase):

    def setUp(self):
        self.fixture = {
            'AllocatedStorage': 123,
            'AvailabilityZones': [
                'string',
            ],
            'BackupRetentionPeriod': 123,
            'CharacterSetName': 'string',
            'DatabaseName': 'string',
            'DBClusterIdentifier': 'string',
            'DBClusterParameterGroup': 'string',
            'DBSubnetGroup': 'string',
            'Status': 'string',
            'AutomaticRestartTime': datetime.datetime(2015, 1, 1),
            'PercentProgress': 'string',
            'EarliestRestorableTime': datetime.datetime(2015, 1, 1),
            'Endpoint': 'string',
            'ReaderEndpoint': 'string',
            'CustomEndpoints': [
                'string',
            ],
            'MultiAZ': True|False,
            'Engine': 'string',
            'EngineVersion': 'string',
            'LatestRestorableTime': datetime.datetime(2015, 1, 1),
            'Port': 123,
            'MasterUsername': 'string',
            'DBClusterOptionGroupMemberships': [
                {
                    'DBClusterOptionGroupName': 'string',
                    'Status': 'string'
                },
            ],
            'PreferredBackupWindow': 'string',
            'PreferredMaintenanceWindow': 'string',
            'ReplicationSourceIdentifier': 'string',
            'ReadReplicaIdentifiers': [
                'string',
            ],
            'DBClusterMembers': [
                {
                    'DBInstanceIdentifier': 'string',
                    'IsClusterWriter': True,
                    'DBClusterParameterGroupStatus': 'string',
                    'PromotionTier': 123
                },
            ],
            'VpcSecurityGroups': [
                {
                    'VpcSecurityGroupId': 'SecurityGroupId1',
                    'Status': 'string'
                },
                {
                    'VpcSecurityGroupId': 'SecurityGroupId2',
                    'Status': 'string'
                },
            ],
            'HostedZoneId': 'string',
            'StorageEncrypted': True,
            'KmsKeyId': 'string',
            'DbClusterResourceId': 'string',
            'DBClusterArn': 'string',
            'AssociatedRoles': [
                {
                    'RoleArn': 'RoleArn1',
                    'Status': 'string',
                    'FeatureName': 'string'
                },
                {
                    'RoleArn': 'RoleArn2',
                    'Status': 'string',
                    'FeatureName': 'string'
                },
            ],
            'IAMDatabaseAuthenticationEnabled': True,
            'CloneGroupId': 'string',
            'ClusterCreateTime': datetime.datetime(2015, 1, 1),
            'EarliestBacktrackTime': datetime.datetime(2015, 1, 1),
            'BacktrackWindow': 123,
            'BacktrackConsumedChangeRecords': 123,
            'EnabledCloudwatchLogsExports': [
                'string',
            ],
            'Capacity': 123,
            'EngineMode': 'string',
            'ScalingConfigurationInfo': {
                'MinCapacity': 123,
                'MaxCapacity': 123,
                'AutoPause': True|False,
                'SecondsUntilAutoPause': 123,
                'TimeoutAction': 'string',
                'SecondsBeforeTimeout': 123
            },
            'DeletionProtection': True,
            'HttpEndpointEnabled': True,
            'ActivityStreamMode': 'sync',
            'ActivityStreamStatus': 'started',
            'ActivityStreamKmsKeyId': 'string',
            'ActivityStreamKinesisStreamName': 'string',
            'CopyTagsToSnapshot': True,
            'CrossAccountClone': True,
            'DomainMemberships': [
                {
                    'Domain': 'string',
                    'Status': 'string',
                    'FQDN': 'string',
                    'IAMRoleName': 'string'
                },
            ],
            'TagList': [
                {
                    'Key': 'Key1',
                    'Value': 'Value1'
                },
                {
                    'Key': 'Key2',
                    'Value': 'Value2'
                },
                {
                    'Key': 'Key3',
                    'Value': 'Value3'
                },
                {
                    'Key': 'KeyN',
                    'Value': 'ValueN'
                },
            ],
            'GlobalWriteForwardingStatus': 'enabled',
            'GlobalWriteForwardingRequested': True,
            'PendingModifiedValues': {
                'PendingCloudwatchLogsExports': {
                    'LogTypesToEnable': [
                        'string',
                    ],
                    'LogTypesToDisable': [
                        'string',
                    ]
                },
                'DBClusterIdentifier': 'string',
                'MasterUserPassword': 'string',
                'IAMDatabaseAuthenticationEnabled': True,
                'EngineVersion': 'string'
            },
            'DBClusterInstanceClass': 'string',
            'StorageType': 'string',
            'Iops': 123,
            'PubliclyAccessible': False,
            'AutoMinorVersionUpgrade': True,
            'MonitoringInterval': 123,
            'MonitoringRoleArn': 'string',
            'PerformanceInsightsEnabled': True,
            'PerformanceInsightsKMSKeyId': 'string',
            'PerformanceInsightsRetentionPeriod': 123
        }
        self.database = lambda_functions.audit_rds.audit_rds.Database(
            self.fixture
        )

    def test_database_name(self):
        self.assertEqual(
            self.database.database_name(),
            self.fixture['DatabaseName']
        )

    def test_dictionary(self):
        self.maxDiff = None
        actual = self.database.to_dict()
        actual.pop('DateAudited')
        self.assertEqual(
            actual,
            {
                'AssociatedIamRoles': 'RoleArn1, RoleArn2',
                'AutoMinorVersionUpgrade': True,
                'AvailabilityZones': 'string',
                'ClusterIdentifier': 'string',
                'DbInstanceClass': 'string',
                'DeletionProtection': True,
                'EncryptedStorage': True,
                'Endpoint': 'string',
                'Engine': 'string',
                'IAMDatabaseAuthenticationEnabled': True,
                'Key1': 'Value1',
                'Key2': 'Value2',
                'Key3': 'Value3',
                'KeyN': 'ValueN',
                'KmsKeyId': 'string',
                'LastRestorableTime': datetime.datetime(2015, 1, 1, 0, 0),
                'MultiAZ': True,
                'PerformanceInsightsEnabled': True,
                'PreferredBackupWindow': 'string',
                'ResourceName': 'string',
                'StorageType': 'string',
                'SecurityGroupIds': 'SecurityGroupId1, SecurityGroupId2',
            }
        )

    def test_handler(self):
        lambda_functions.audit_rds.audit_rds.handler(None, None)