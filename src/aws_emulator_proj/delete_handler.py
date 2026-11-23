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
        deleted = repository.delete_movie(ids["movie_id"])
    elif resource == "/series/{series_id}":
        deleted = repository.delete_series(ids["series_id"])
    elif resource == "/series/{series_id}/season/{season_number}":
        deleted = repository.delete_season(ids["series_id"], ids["season_number"])
    else:
        deleted = repository.delete_episode(
            ids["series_id"], ids["season_number"], ids["episode_number"]
        )

    if not deleted:
        return response(404, {"message": "Not found"})
    logger.info("Deleted", extra={"resource": resource, "ids": ids})
    return {"statusCode": 204, "body": ""}


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }