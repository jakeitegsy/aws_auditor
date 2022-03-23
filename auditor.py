import constructs
import aws_cdk


class Inventory(aws_cdk.Stack):

    def __init__(
        self, scope: constructs.Construct, construct_id: str,
        auditor_name=None, actions=None, sort_key=None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Make Lambda VPC based
        auditor = aws_cdk.aws_lambda.Function(
            self, f'{auditor_name}LambdaFunction',
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_9,
            function_name=auditor_name,
            handler=f'{auditor_name}.handler',
            code=aws_cdk.aws_lambda.Code.from_asset(f'lambda_functions/{auditor_name}'),
        )

        audit_records = aws_cdk.aws_dynamodb.Table(
            self, f'{auditor_name}Records',
            table_name=auditor_name,
            sort_key=sort_key,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
            billing_mode=aws_cdk.BillingMode.PAY_PER_REQUEST,
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name='name',
                type=aws_cdk.aws_dynamodb.AttributeType.STRING
            ),
        )

        audit_records.grant(auditor, 'dynamodb:PutItem')

        # add scheduled event to lambda function