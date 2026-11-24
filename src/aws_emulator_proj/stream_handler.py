from aws_lambda_powertools import Logger

logger = Logger()

def handler(event, context):
    for record in event["Records"]:
        keys = record["dynamodb"]["Keys"]
        logger.info(
            "Table changed",
            extra={"change": record["eventName"], "PK": keys["PK"]["S"], "SK": keys["SK"]["S"]},
        )