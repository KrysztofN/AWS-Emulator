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

data "archive_file" "placeholder" {
  type        = "zip"
  output_path = "${path.module}/placeholder.zip"

  source {
    filename = "aws_emulator_proj/upload_handler.py"
    content  = "def handler(event, context):\n    pass\n"
  }
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