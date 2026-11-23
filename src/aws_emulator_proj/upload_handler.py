from aws_lambda_powertools import Logger
from aws_emulator_proj.events import UploadEventParser

logger = Logger()
parser = UploadEventParser()

def handler(event, context):
    for uploaded_file in parser.parse(event):
        logger.info(
            "Received upload",
            extra={"bucket": uploaded_file.bucket, "key": uploaded_file.key},
        )