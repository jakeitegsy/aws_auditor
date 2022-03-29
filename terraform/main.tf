provider "aws" {
    region = var.aws_region
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

resource "aws_dynamodb_table" "inventory" {
    name = "audit_lambda"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "ResourceName"

    attribute {
        name="ResourceName"
        type="S"
    }

    tags = {
        Name = "audit_lambda"
    }
}

data "aws_iam_policy_document" "audit_lambda_policy" {
    statement {
        actions = ["sts:AssumeRole"]
        effect = "Allow"
        principals {
            type = "Service"
            identities = ["lambda.amazonaws.com"]
        }
    }
}

data "archive_file" "audit_lambda_package" {
    type = "zip"
    source_dir = "lambda_functions/audit_lambda"
    output_path = "lambda_functions/audit_lambda/audit_lambda.zip"
    excludes = ["lambda_functions/audit_lambda/audit_lambda.zip", "lambda_functions/audit_lambda/tests"]
}

resource "aws_iam_role" "audit_lambda" {
    name = "audit_lambda_role"
    assume_role_policy = data.aws_iam_policy_document.audit_lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "audit_lambda_managed_policy" {
    role = aws_iam_role.audit_lambda_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "audit_lambda" {
    description = "audit lambda functions"
    filename = data.archive_file.audit_lambda_package.output_path
    source_code_hash = data.archive_file.audit_lambda.output_base64sha256
    function_name = "audit_lambda"
    handler = "audit_lambda.handler"
    role = aws_iam_role.audit_lambda_role.arn
    runtime = "python3.9"

    environment {
        variables = {
            "AWS_REGION" = data.aws_region.current,
            "INVENTORY_TABLE_NAME" = aws_dynamodb_table.audit_lambda.name,
        }
    }

    tags = {
        Name = "audit_lambda"
    }
}