import json
import os
from aws_lambda_powertools import Logger
from aws_emulator_proj.repository import MediaRepository

logger = Logger()
repository = MediaRepository(os.environ["TABLE_NAME"])


def handler(event, context):
    movie_id = event["pathParameters"]["movie_id"]
    if not movie_id.isdigit():
        return response(400, {"message": "movie_id must be a number"})

    movie = repository.get_movie(int(movie_id))
    if movie is None:
        return response(404, {"message": "Movie not found"})

    return response(200, movie)


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=decimal_to_number),
    }


def decimal_to_number(value):
    return int(value) if value % 1 == 0 else float(value)