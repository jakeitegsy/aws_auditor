import boto3
import datetime
import os

CLOUDWATCH = boto3.client("cloudwatch")
PAGINATED_LIST_OF_ALARMS = CLOUDWATCH.get_paginator("describe_alarms")
TABLE = boto3.resource(
    "dynamodb",
).Table(os.environ.get("INVENTORY_TABLE_NAME"))


def to_dict(metric_alarm):
    for key, value in metric_alarm.items():
        if isinstance(value, datetime.datetime):
            metric_alarm[key] = str(value)
    metric_alarm.update({"DateAudited": str(datetime.datetime.now())})
    return metric_alarm


def list_alarms():
    return (
        alarm
        for page in PAGINATED_LIST_OF_ALARMS.paginate()
        for alarm in page["MetricAlarms"]
    )


def handler(event, context):
    for metric_alarm in list_alarms():
        TABLE.put_item(Item=to_dict(metric_alarm))
