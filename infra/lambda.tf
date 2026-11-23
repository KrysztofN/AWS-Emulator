# Upload Lambda
resource "aws_iam_role" "upload_lambda" {
  name = "upload-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "upload_lambda_sqs" {
  role       = aws_iam_role.upload_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
}

resource "aws_lambda_function" "upload" {
  function_name                  = "upload"
  role                           = aws_iam_role.upload_lambda.arn
  runtime                        = "python3.12"
  handler                        = "aws_emulator_proj.upload_handler.handler"
  filename                       = data.archive_file.placeholder.output_path
  timeout                        = 30
  reserved_concurrent_executions = 1

  environment {
    variables = {
      POWERTOOLS_SERVICE_NAME = "upload"
    }
  }

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}

resource "aws_lambda_event_source_mapping" "upload" {
  event_source_arn = aws_sqs_queue.uploads.arn
  function_name    = aws_lambda_function.upload.arn
  batch_size       = 1
}

# Put lambda
resource "aws_iam_role" "put_lambda" {
  name = "put-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "put_lambda" {
  name = "put-lambda"
  role = aws_iam_role.put_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
        ]
        Resource = aws_sqs_queue.put.arn
      },
      {
        Effect   = "Allow"
        Action   = "dynamodb:PutItem"
        Resource = aws_dynamodb_table.media.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Resource = "*"
      },
    ]
  })
}

resource "aws_lambda_function" "put" {
  function_name = "put"
  role          = aws_iam_role.put_lambda.arn
  runtime       = "python3.12"
  handler       = "aws_emulator_proj.put_handler.handler"
  filename      = data.archive_file.placeholder.output_path
  timeout       = 30

  environment {
    variables = {
      POWERTOOLS_SERVICE_NAME = "put"
      TABLE_NAME              = aws_dynamodb_table.media.name
    }
  }

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}

resource "aws_lambda_event_source_mapping" "put" {
  event_source_arn = aws_sqs_queue.put.arn
  function_name    = aws_lambda_function.put.arn
  batch_size       = 1
}

data "archive_file" "placeholder" {
  type        = "zip"
  output_path = "${path.module}/placeholder.zip"

  source {
    filename = "aws_emulator_proj/upload_handler.py"
    content  = "def handler(event, context):\n    pass\n"
  }

  source {
    filename = "aws_emulator_proj/put_handler.py"
    content  = "def handler(event, context):\n    pass\n"
  }
}