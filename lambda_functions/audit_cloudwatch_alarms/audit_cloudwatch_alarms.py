import boto3
import datetime
import os


class MetricAlarm:

    def __init__(self, metric_alarm):
        self.metric_alarm = metric_alarm

    def get(self, key, value=None):
        try:
            return self.metric_alarm[key]
        except KeyError:
            return value

    def alarm_name(self):
        return self.get('AlarmName')

    @staticmethod
    def stringify(iterable):
        return ', '.join(iterable)

    def to_dict(self):
        return {
            'ResourceName': self.alarm_name(),
            'DateAudited': str(datetime.datetime.now()),
            'AlarmArn': self.get('AlarmArn'),
            'AlarmDescription': self.get('AlarmDescription'),
            'AlarmConfigurationUpdatedTimestamp': str(self.get('AlarmConfigurationUpdatedTimestamp')),
            'ActionsEnabled': self.get('ActionsEnabled'),
            'AlarmActions': self.stringify(self.get('AlarmActions')),
            'OKActions': self.stringify(self.get('OKActions')),
            'InsufficientDataActions': self.stringify(self.get('InsufficientDataActions')),
            'StateValue': self.get('StateValue'),
            'StateReason': self.get('StateReason'),
            'MetricName': self.get('MetricName'),
            'Namespace': self.get('Namespace'),
            'Statistic': self.get('Statistic'),
            'ExtendedStatistic': self.get('ExtendedStatistic'),
            'Period': self.get('Period'),
            'EvaluationPeriods': self.get('EvaluationPeriods'),
            'Unit': self.get('Unit'),
            'DatapointsToAlarm': self.get('DatapointsToAlarm'),
            'Threshold': str(self.get('Threshold')),
            'ComparisonOperator': self.get('ComparisonOperator'),
        }


def region():
    return os.environ.get('REGION')

def list_alarms():
    return (
        alarm for page in PAGINATED_LIST_OF_ALARMS.paginate()
        for alarm in page['MetricAlarms']
    )

def write_to_dynamodb(data):
    return TABLE.put_item(Item=MetricAlarm(data).to_dict())

def handler(event, context):
    for alarm in list_alarms():
        TABLE.put_item(
            Item=MetricAlarm(alarm).to_dict()
        )

CLOUDWATCH = boto3.client("cloudwatch")
PAGINATED_LIST_OF_ALARMS = CLOUDWATCH.get_paginator("describe_alarms")
TABLE = boto3.resource(
    'dynamodb',
    endpoint_url=f'https://dynamodb.{region()}.amazonaws.com'
).Table(
    os.environ.get('INVENTORY_TABLE_NAME')
)