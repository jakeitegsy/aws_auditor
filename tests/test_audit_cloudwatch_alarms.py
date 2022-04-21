import sys
import os

sys.path.insert(0, os.path.abspath(".."))
import mock_boto3

sys.modules["boto3"] = mock_boto3
os.environ["INVENTORY_TABLE_NAME"] = "audit-lambda"

import unittest
import datetime
import lambda_functions.audit_cloudwatch_alarms.audit_cloudwatch_alarms


class TestAuditRds(unittest.TestCase):
    def setUp(self):
        self.fixture = {
            "AlarmName": "AlarmName",
            "AlarmArn": "AlarmArn",
            "AlarmDescription": "AlarmDescription",
            "AlarmConfigurationUpdatedTimestamp": datetime.datetime(2015, 1, 1),
            "ActionsEnabled": True,
            "OKActions": [
                "OKAction1",
                "OKActionN",
            ],
            "AlarmActions": [
                "AlarmAction1",
                "AlarmActionN",
            ],
            "InsufficientDataActions": [
                "InsufficientDataAction1",
                "InsufficientDataActionN",
            ],
            "StateValue": "OK",
            "StateReason": "string",
            "StateReasonData": "string",
            "StateUpdatedTimestamp": datetime.datetime(2015, 1, 1),
            "MetricName": "string",
            "Namespace": "string",
            "Statistic": "Sum",
            "ExtendedStatistic": "string",
            "Dimensions": [
                {"Name": "Dimension1", "Value": "Value1"},
                {"Name": "Dimension2", "Value": "Value2"},
            ],
            "Period": 123,
            "Unit": "Bits",
            "EvaluationPeriods": 123,
            "DatapointsToAlarm": 123,
            "Threshold": 123.0,
            "ComparisonOperator": "GreaterThanOrEqualToThreshold",
            "TreatMissingData": "string",
            "EvaluateLowSampleCountPercentile": "string",
            "Metrics": [
                {
                    "Id": "MetricId",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": "Namespace",
                            "MetricName": "MetricName",
                            "Dimensions": [
                                {"Name": "Dimension1", "Value": "Value1"},
                                {"Name": "DimensionN", "Value": "ValueN"},
                            ],
                        },
                        "Period": 123,
                        "Stat": "string",
                        "Unit": "Seconds",
                    },
                    "Expression": "Expression",
                    "Label": "Label",
                    "ReturnData": True,
                    "Period": 123,
                    "AccountId": "AccountId",
                },
            ],
            "ThresholdMetricId": "string",
        }
        self.metric_alarm = lambda_functions.audit_cloudwatch_alarms.audit_cloudwatch_alarms.MetricAlarm(
            self.fixture
        )

    def test_database_name(self):
        self.assertEqual(self.metric_alarm.alarm_name(), self.fixture["AlarmName"])

    def test_dictionary(self):
        self.maxDiff = None
        actual = self.metric_alarm.to_dict()
        actual.pop("DateAudited")
        self.assertEqual(
            actual,
            {
                "AlarmName": "AlarmName",
                "AlarmArn": "AlarmArn",
                "AlarmDescription": "AlarmDescription",
                "AlarmConfigurationUpdatedTimestamp": str(datetime.datetime(2015, 1, 1)),
                "ActionsEnabled": True,
                "OKActions": [
                    "OKAction1",
                    "OKActionN",
                ],
                "AlarmActions": [
                    "AlarmAction1",
                    "AlarmActionN",
                ],
                "InsufficientDataActions": [
                    "InsufficientDataAction1",
                    "InsufficientDataActionN",
                ],
                "StateValue": "OK",
                "StateReason": "string",
                "StateReasonData": "string",
                "StateUpdatedTimestamp": str(datetime.datetime(2015, 1, 1)),
                "MetricName": "string",
                "Namespace": "string",
                "Statistic": "Sum",
                "ExtendedStatistic": "string",
                "Dimensions": [
                    {"Name": "Dimension1", "Value": "Value1"},
                    {"Name": "Dimension2", "Value": "Value2"},
                ],
                "Period": 123,
                "Unit": "Bits",
                "EvaluationPeriods": 123,
                "DatapointsToAlarm": 123,
                "Threshold": 123.0,
                "ComparisonOperator": "GreaterThanOrEqualToThreshold",
                "TreatMissingData": "string",
                "EvaluateLowSampleCountPercentile": "string",
                "Metrics": [
                    {
                        "Id": "MetricId",
                        "MetricStat": {
                            "Metric": {
                                "Namespace": "Namespace",
                                "MetricName": "MetricName",
                                "Dimensions": [
                                    {"Name": "Dimension1", "Value": "Value1"},
                                    {"Name": "DimensionN", "Value": "ValueN"},
                                ],
                            },
                            "Period": 123,
                            "Stat": "string",
                            "Unit": "Seconds",
                        },
                        "Expression": "Expression",
                        "Label": "Label",
                        "ReturnData": True,
                        "Period": 123,
                        "AccountId": "AccountId",
                    },
                ],
                "ThresholdMetricId": "string",
            },
        )
