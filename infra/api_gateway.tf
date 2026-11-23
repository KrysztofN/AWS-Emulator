locals {
  account_id = split(":", aws_sqs_queue.put.arn)[4]
}

resource "aws_iam_role" "api_gateway" {
  name = "api-gateway"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "apigateway.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "api_gateway" {
  name = "api-gateway"
  role = aws_iam_role.api_gateway.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "sqs:SendMessage"
        Resource = aws_sqs_queue.put.arn
      }
    ]
  })
}

resource "aws_api_gateway_rest_api" "media" {
  name = "media"

  body = templatefile("${path.module}/openapi.json.tftpl", {
    account_id           = local.account_id
    put_queue_name       = aws_sqs_queue.put.name
    api_gateway_role_arn = aws_iam_role.api_gateway.arn
    get_function_arn     = aws_lambda_function.get.arn
    delete_function_arn  = aws_lambda_function.delete.arn
  })
}

resource "aws_api_gateway_deployment" "media" {
  rest_api_id = aws_api_gateway_rest_api.media.id

  triggers = {
    redeployment = sha1(aws_api_gateway_rest_api.media.body)
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "dev" {
  rest_api_id   = aws_api_gateway_rest_api.media.id
  deployment_id = aws_api_gateway_deployment.media.id
  stage_name    = "dev"
}