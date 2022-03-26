import constructs
import aws_cdk
import utilities


class Inventory(aws_cdk.Stack):

    def __init__(
        self, scope: constructs.Construct, construct_id: str,
        auditor_name=None, actions=None, sort_key=None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        audit_inventory = aws_cdk.aws_dynamodb.Table(
            self, utilities.hyphenate(f'{auditor_name.title()}DynamoDBTable'),
            table_name=auditor_name,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
            billing_mode=aws_cdk.aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name='name',
                type=aws_cdk.aws_dynamodb.AttributeType.STRING
            ),
            sort_key=self.get_sort_key(sort_key),
        )

        # Make Lambda VPC based
        auditor = aws_cdk.aws_lambda.Function(
            self, utilities.hyphenate(f'{auditor_name.title()}LambdaFunction'),
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_9,
            function_name=auditor_name,
            handler=f'{auditor_name}.handler',
            code=aws_cdk.aws_lambda.Code.from_asset(
                f'lambda_functions/{auditor_name}'
            ),
            environment={
                'AWS_REGION': self.region,
                'INVENTORY_TABLE_NAME': audit_inventory.table_name,
            },
        )

        auditor.add_to_role_policy(
            aws_cdk.aws_iam.PolicyStatement(
                effect=aws_cdk.aws_iam.Effect.ALLOW,
                actions=actions,
                resources=["*"],
            )
        )
        audit_inventory.grant(auditor, 'dynamodb:PutItem')

        # add scheduled event to lambda function

    @staticmethod
    def get_sort_key(sort_key):
        return sort_key if sort_key is None else aws_cdk.aws_dynamodb.Attribute(
            name=sort_key,
            type=aws_cdk.aws_dynamodb.AttributeType.STRING
        )