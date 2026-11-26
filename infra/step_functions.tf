resource "aws_iam_role" "remove_movie" {
  name = "remove-movie"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "states.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "remove_movie" {
  role = aws_iam_role.remove_movie.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "lambda:InvokeFunction"
      Resource = [aws_lambda_function.get.arn, aws_lambda_function.delete.arn]
    }]
  })
}

resource "aws_sfn_state_machine" "remove_movie" {
  name     = "remove-movie"
  role_arn = aws_iam_role.remove_movie.arn
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
        ResultPath = "$.found"
        Next       = "IsFound"
      }
      IsFound = {
        Type    = "Choice"
        Choices = [{ Variable = "$.found.Payload.statusCode", NumericEquals = 200, Next = "DeleteMovie" }]
        Default = "NotFound"
      }
      DeleteMovie = {
        Type     = "Task"
        Resource = "arn:aws:states:::lambda:invoke"
        Parameters = {
          FunctionName = aws_lambda_function.delete.arn
          Payload = {
            resource       = "/movies/{movie_id}"
            pathParameters = { "movie_id.$" = "$.movie_id" }
          }
        }
        OutputPath = "$.Payload"
        End        = true
      }
      NotFound = { Type = "Fail", Error = "MovieNotFound" }
    }
  })
}

output "remove_movie_arn" {
  value = aws_sfn_state_machine.remove_movie.arn
}