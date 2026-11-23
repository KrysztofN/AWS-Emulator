import json
import os
from aws_lambda_powertools import Logger
from aws_emulator_proj.repository import MediaRepository

logger = Logger()
repository = MediaRepository(os.environ["TABLE_NAME"])


def handler(event, context):
    parameters = event["pathParameters"]
    if not all(value.isdigit() for value in parameters.values()):
        return response(400, {"message": "Path parameters must be numbers"})
    ids = {name: int(value) for name, value in parameters.items()}

    resource = event["resource"]
    if resource == "/movies/{movie_id}":
        item = repository.get_movie(ids["movie_id"])
    elif resource == "/series/{series_id}":
        item = repository.get_series(ids["series_id"])
    elif resource == "/series/{series_id}/season/{season_number}":
        item = repository.get_season(ids["series_id"], ids["season_number"])
    else:
        item = repository.get_episode(ids["series_id"], ids["season_number"], ids["episode_number"])

    if item is None:
        return response(404, {"message": "Not found"})
    return response(200, item)


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=decimal_to_number),
    }


def decimal_to_number(value):
    return int(value) if value % 1 == 0 else float(value)