from aws_lambda_powertools import Logger

logger = Logger()

def handler(event, context):
    logger.info("Received event", extra={"event": event})