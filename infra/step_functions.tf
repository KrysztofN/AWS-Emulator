resource "aws_iam_role" "verify_movie" {
  name = "verify-movie"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "states.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "verify_movie" {
  role = aws_iam_role.verify_movie.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "lambda:InvokeFunction"
      Resource = aws_lambda_function.get.arn
    }]
  })
}

resource "aws_sfn_state_machine" "verify_movie" {
  name     = "verify-movie"
  role_arn = aws_iam_role.verify_movie.arn
  definition = jsonencode({
    StartAt = "GetMovie"
    States = {
      GetMovie = {
        Type     = "Task"
        Resource = "arn:aws:states:::lambda:invoke"
        Parameters = {
          FunctionName = aws_lambda_function.get.arn
          Payload = {
            resource       = "/movies/{movie_id}"
            pathParameters = { "movie_id.$" = "$.movie_id" }
          }
        }
        OutputPath = "$.Payload"
        End        = true
      }
    }
  })
}

output "verify_movie_arn" {
  value = aws_sfn_state_machine.verify_movie.arn
}