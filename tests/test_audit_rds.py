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
            'DBInstanceIdentifier': 'string',
            'DBInstanceClass': 'string',
            'Engine': 'string',
            'DBInstanceStatus': 'string',
            'AutomaticRestartTime': datetime.datetime(2015, 1, 1),
            'MasterUsername': 'string',
            'DBName': 'string',
            'Endpoint': {
                'Address': 'string',
                'Port': 123,
                'HostedZoneId': 'string'
            },
            'AllocatedStorage': 123,
            'InstanceCreateTime': datetime.datetime(2015, 1, 1),
            'PreferredBackupWindow': 'string',
            'BackupRetentionPeriod': 123,
            'DBSecurityGroups': [
                {
                    'DBSecurityGroupName': 'SecurityGroupId1',
                    'Status': 'string'
                },
                {
                    'DBSecurityGroupName': 'SecurityGroupId2',
                    'Status': 'string'
                },
                {
                    'DBSecurityGroupName': 'SecurityGroupId3',
                    'Status': 'string'
                },
                {
                    'DBSecurityGroupName': 'SecurityGroupIdN',
                    'Status': 'string'
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
                {
                    'VpcSecurityGroupId': 'SecurityGroupId3',
                    'Status': 'string'
                },
                {
                    'VpcSecurityGroupId': 'SecurityGroupIdN',
                    'Status': 'string'
                },
            ],
            'DBParameterGroups': [
                {
                    'DBParameterGroupName': 'string',
                    'ParameterApplyStatus': 'string'
                },
            ],
            'AvailabilityZone': 'string',
            'DBSubnetGroup': {
                'DBSubnetGroupName': 'string',
                'DBSubnetGroupDescription': 'string',
                'VpcId': 'string',
                'SubnetGroupStatus': 'string',
                'Subnets': [
                    {
                        'SubnetIdentifier': 'string',
                        'SubnetAvailabilityZone': {
                            'Name': 'string'
                        },
                        'SubnetOutpost': {
                            'Arn': 'string'
                        },
                        'SubnetStatus': 'string'
                    },
                ],
                'DBSubnetGroupArn': 'string'
            },
            'PreferredMaintenanceWindow': 'string',
            'PendingModifiedValues': {
                'DBInstanceClass': 'string',
                'AllocatedStorage': 123,
                'MasterUserPassword': 'string',
                'Port': 123,
                'BackupRetentionPeriod': 123,
                'MultiAZ': True,
                'EngineVersion': 'string',
                'LicenseModel': 'string',
                'Iops': 123,
                'DBInstanceIdentifier': 'string',
                'StorageType': 'string',
                'CACertificateIdentifier': 'string',
                'DBSubnetGroupName': 'string',
                'PendingCloudwatchLogsExports': {
                    'LogTypesToEnable': [
                        'string',
                    ],
                    'LogTypesToDisable': [
                        'string',
                    ]
                },
                'ProcessorFeatures': [
                    {
                        'Name': 'string',
                        'Value': 'string'
                    },
                ],
                'IAMDatabaseAuthenticationEnabled': True,
                'AutomationMode': 'full',
                'ResumeFullAutomationModeTime': datetime.datetime(2015, 1, 1)
            },
            'LatestRestorableTime': datetime.datetime(2015, 1, 1),
            'MultiAZ': True,
            'EngineVersion': 'string',
            'AutoMinorVersionUpgrade': True,
            'ReadReplicaSourceDBInstanceIdentifier': 'string',
            'ReadReplicaDBInstanceIdentifiers': [
                'string',
            ],
            'ReadReplicaDBClusterIdentifiers': [
                'string',
            ],
            'ReplicaMode': 'open-read-only',
            'LicenseModel': 'string',
            'Iops': 123,
            'OptionGroupMemberships': [
                {
                    'OptionGroupName': 'string',
                    'Status': 'string'
                },
            ],
            'CharacterSetName': 'string',
            'NcharCharacterSetName': 'string',
            'SecondaryAvailabilityZone': 'string',
            'PubliclyAccessible': True,
            'StatusInfos': [
                {
                    'StatusType': 'string',
                    'Normal': True,
                    'Status': 'string',
                    'Message': 'string'
                },
            ],
            'StorageType': 'string',
            'TdeCredentialArn': 'string',
            'DbInstancePort': 123,
            'DBClusterIdentifier': 'string',
            'StorageEncrypted': True,
            'KmsKeyId': 'string',
            'DbiResourceId': 'string',
            'CACertificateIdentifier': 'string',
            'DomainMemberships': [
                {
                    'Domain': 'string',
                    'Status': 'string',
                    'FQDN': 'string',
                    'IAMRoleName': 'string'
                },
            ],
            'CopyTagsToSnapshot': True,
            'MonitoringInterval': 123,
            'EnhancedMonitoringResourceArn': 'string',
            'MonitoringRoleArn': 'string',
            'PromotionTier': 123,
            'DBInstanceArn': 'string',
            'Timezone': 'string',
            'IAMDatabaseAuthenticationEnabled': True,
            'PerformanceInsightsEnabled': True,
            'PerformanceInsightsKMSKeyId': 'string',
            'PerformanceInsightsRetentionPeriod': 123,
            'EnabledCloudwatchLogsExports': [
                'string',
            ],
            'ProcessorFeatures': [
                {
                    'Name': 'string',
                    'Value': 'string'
                },
            ],
            'DeletionProtection': True,
            'AssociatedRoles': [
                {
                    'RoleArn': 'RoleArn1',
                    'FeatureName': 'string',
                    'Status': 'string'
                },
                {
                    'RoleArn': 'RoleArn2',
                    'FeatureName': 'string',
                    'Status': 'string'
                },
                {
                    'RoleArn': 'RoleArn3',
                    'FeatureName': 'string',
                    'Status': 'string'
                },
                {
                    'RoleArn': 'RoleArnN',
                    'FeatureName': 'string',
                    'Status': 'string'
                },
            ],
            'ListenerEndpoint': {
                'Address': 'string',
                'Port': 123,
                'HostedZoneId': 'string'
            },
            'MaxAllocatedStorage': 123,
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
            'DBInstanceAutomatedBackupsReplications': [
                {
                    'DBInstanceAutomatedBackupsArn': 'string'
                },
            ],
            'CustomerOwnedIpEnabled': True,
            'AwsBackupRecoveryPointArn': 'string',
            'ActivityStreamStatus': 'stopped',
            'ActivityStreamKmsKeyId': 'string',
            'ActivityStreamKinesisStreamName': 'string',
            'ActivityStreamMode': 'sync',
            'ActivityStreamEngineNativeAuditFieldsIncluded': True|False,
            'AutomationMode': 'full',
            'ResumeFullAutomationModeTime': datetime.datetime(2015, 1, 1),
            'CustomIamInstanceProfile': 'string',
            'BackupTarget': 'string'
        }
        self.database = lambda_functions.audit_rds.audit_rds.Database(
            self.fixture
        )

    def test_database_name(self):
        self.assertEqual(
            self.database.database_name(),
            self.fixture['DBName']
        )

    def test_dictionary(self):
        self.maxDiff = None
        actual = self.database.to_dict()
        actual.pop('DateAudited')
        self.assertEqual(
            actual,
            {
                'AssociatedIamRoles': 'RoleArn1, RoleArn2, RoleArn3, RoleArnN',
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
                'LastRestorableTime': str(datetime.datetime(2015, 1, 1, 0, 0)),
                'MultiAZ': True,
                'PerformanceInsightsEnabled': True,
                'PreferredBackupWindow': 'string',
                'ResourceName': 'string',
                'StorageType': 'string',
                'VPCSecurityGroupIds': 'SecurityGroupId1, SecurityGroupId2, SecurityGroupId3, SecurityGroupIdN',
                'DBSecurityGroupIds': 'SecurityGroupId1, SecurityGroupId2, SecurityGroupId3, SecurityGroupIdN',
            }
        )

    def test_handler(self):
        lambda_functions.audit_rds.audit_rds.handler(None, None)