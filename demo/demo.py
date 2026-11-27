import sys

import boto3


def handler(event, context):
    if event["test"] == "python":
        return sys.version
    return boto3.client("s3").list_objects_v2(Bucket="media-files", Prefix="reports/")["KeyCount"]