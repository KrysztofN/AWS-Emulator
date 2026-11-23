import json
from urllib.parse import unquote_plus

class UploadedFile:
    def __init__(self, bucket: str, key: str):
        self.bucket = bucket
        self.key = key


class UploadEventParser:
    def parse(self, event: dict) -> list[UploadedFile]:
        files = []
        for message in event["Records"]:
            s3_event = json.loads(message["body"])
            for record in s3_event.get("Records", []):
                files.append(
                    UploadedFile(
                        bucket=record["s3"]["bucket"]["name"],
                        key=unquote_plus(record["s3"]["object"]["key"]),
                    )
                )
        return files