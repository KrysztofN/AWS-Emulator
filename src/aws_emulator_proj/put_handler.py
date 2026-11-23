import json
import os
from decimal import Decimal
from aws_lambda_powertools import Logger
from aws_emulator_proj.repository import MediaRepository

logger = Logger()
repository = MediaRepository(os.environ["TABLE_NAME"])

def handler(event, context):
    for record in event["Records"]:
        try:
            save_movie(record)
        except (KeyError, ValueError, TypeError) as error:
            logger.error("Rejected invalid message", extra={"error": repr(error)})


def save_movie(record):
    movie_id = int(record["messageAttributes"]["movie_id"]["stringValue"])
    metadata = json.loads(record["body"], parse_float=Decimal)
    repository.put_movie(movie_id, metadata)
    logger.info("Saved movie", extra={"movie_id": movie_id})