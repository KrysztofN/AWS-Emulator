resource "aws_sqs_queue" "uploads" {
  name = "media-uploads"
}

resource "aws_sqs_queue_policy" "uploads" {
  queue_url = aws_sqs_queue.uploads.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "s3.amazonaws.com" }
        Action    = "sqs:SendMessage"
        Resource  = aws_sqs_queue.uploads.arn
        Condition = {
          ArnEquals = { "aws:SourceArn" = aws_s3_bucket.media_files.arn }
        }
      }
    ]
  })
}