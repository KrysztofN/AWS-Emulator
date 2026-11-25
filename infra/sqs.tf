resource "aws_sqs_queue" "uploads_dlq" {
  name = "media-uploads-dlq"
}

resource "aws_sqs_queue" "uploads" {
  name                       = "media-uploads"
  visibility_timeout_seconds = 180

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.uploads_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue_policy" "uploads" {
  queue_url = aws_sqs_queue.uploads.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "s3.amazonaws.com" }
      Action    = "sqs:SendMessage"
      Resource  = aws_sqs_queue.uploads.arn
      Condition = {
        ArnEquals = { "aws:SourceArn" = aws_s3_bucket.media_files.arn }
      }
    }]
  })
}

resource "aws_sqs_queue" "put_dlq" {
  name = "media-put-dlq"
}

resource "aws_sqs_queue" "put" {
  name                       = "media-put"
  visibility_timeout_seconds = 180

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.put_dlq.arn
    maxReceiveCount     = 3
  })
}