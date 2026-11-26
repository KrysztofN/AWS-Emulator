resource "aws_cloudwatch_metric_alarm" "large_upload" {
  alarm_name          = "large-upload"
  namespace           = "Media"
  metric_name         = "AcceptedFiles"
  statistic           = "Maximum"
  period              = 60
  evaluation_periods  = 1
  threshold           = 50
  comparison_operator = "GreaterThanThreshold"
}