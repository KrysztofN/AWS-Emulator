resource "aws_s3_bucket" "media_files" {
  bucket = "media-files"
}

resource "aws_s3_bucket_notification" "uploads" {
  bucket = aws_s3_bucket.media_files.id

  queue {
    queue_arn     = aws_sqs_queue.uploads.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "uploads/"
    filter_suffix = ".zip"
  }
}