import boto3


RDS = boto3.session.Session(region_name=region()).client('rds')
PAGINATED_LIST_OF_FUNCTIONS = LAMBDA.get_paginator('list_functions')
TABLE = boto3.resource(
    'dynamodb',
    endpoint_url=f'https://dynamodb.{region()}.amazonaws.com'
).Table(
    os.environ.get('INVENTORY_TABLE_NAME')
)
