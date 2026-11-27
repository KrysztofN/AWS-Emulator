data "archive_file" "demo" {
  type        = "zip"
  source_file = "${path.module}/../demo/demo.py"
  output_path = "${path.module}/demo.zip"
}

resource "aws_iam_role" "demo" {
  name = "demo"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "demo" {
  role = aws_iam_role.demo.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      Resource = "*"
    }]
  })
}

resource "aws_lambda_function" "demo" {
  function_name    = "demo"
  role             = aws_iam_role.demo.arn
  runtime          = "python3.12"
  handler          = "demo.handler"
  timeout          = 30
  filename         = data.archive_file.demo.output_path
  source_code_hash = data.archive_file.demo.output_base64sha256
}