import os

import boto3
from aws_lambda_powertools import Logger

from aws_emulator_proj.events import UploadEventParser
from aws_emulator_proj.upload_import import ArchiveParser, PutQueueSender

logger = Logger()
s3 = boto3.client("s3")
event_parser = UploadEventParser()
archive_parser = ArchiveParser()
sender = PutQueueSender(os.environ["PUT_QUEUE_URL"])

def handler(event, context):
    for uploaded_file in event_parser.parse(event):
        archive = s3.get_object(Bucket=uploaded_file.bucket, Key=uploaded_file.key)["Body"].read()
        messages = archive_parser.parse(archive)
        for message in messages:
            sender.send(message)
        logger.info("Imported upload", extra={"key": uploaded_file.key, "messages": len(messages)})