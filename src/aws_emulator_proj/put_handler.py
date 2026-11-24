import json
import os
from decimal import Decimal
from aws_lambda_powertools import Logger
from aws_emulator_proj.repository import MediaRepository

logger = Logger()
repository = MediaRepository(os.environ["TABLE_NAME"])

def handler(event, context):
    for record in event["Records"]:
        save(record)

def save(record: dict) -> None:
    attributes = record["messageAttributes"]
    entity_type = attributes["type"]["stringValue"]
    metadata = json.loads(record["body"], parse_float=Decimal)

    if entity_type == "movie":
        repository.put_movie(number(attributes, "movie_id"), metadata)
    elif entity_type == "series":
        repository.put_series(number(attributes, "series_id"), metadata)
    elif entity_type == "season":
        repository.put_season(number(attributes, "series_id"), number(attributes, "season_number"), metadata)
    elif entity_type == "episode":
        repository.put_episode(
            number(attributes, "series_id"),
            number(attributes, "season_number"),
            number(attributes, "episode_number"),
            metadata,
        )
    else:
        raise ValueError(f"Unknown type: {entity_type}")

    logger.info("Saved", extra={"type": entity_type})


def number(attributes: dict, name: str) -> int:
    return int(attributes[name]["stringValue"])