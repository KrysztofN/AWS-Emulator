import os
import json
import boto3
from aws_lambda_powertools import Logger

from aws_emulator_proj.events import UploadEventParser
from aws_emulator_proj.upload_import import ArchiveParser, PutQueueSender

logger = Logger()
s3 = boto3.client("s3")
cloudwatch = boto3.client("cloudwatch")
event_parser = UploadEventParser()
archive_parser = ArchiveParser()
sender = PutQueueSender(os.environ["PUT_QUEUE_URL"])

def handler(event, context):
    for uploaded_file in event_parser.parse(event):
        archive = s3.get_object(Bucket=uploaded_file.bucket, Key=uploaded_file.key)["Body"].read()
        messages = archive_parser.parse(archive)
        for message in messages:
            sender.send(message)
        name = uploaded_file.key.removeprefix("uploads/").removesuffix(".zip")
        report = {"source": uploaded_file.key, "status": "accepted", "accepted": len(messages)}
        s3.put_object(Bucket=uploaded_file.bucket, Key=f"reports/{name}.json", Body=json.dumps(report))
        cloudwatch.put_metric_data(Namespace="Media",MetricData=[{"MetricName": "AcceptedFiles", "Value": len(messages), "Unit": "Count"}],)
        logger.info("Imported upload", extra={"key": uploaded_file.key, "messages": len(messages)})