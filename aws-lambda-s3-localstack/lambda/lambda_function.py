import os
import json
import base64

import boto3

BUCKET = os.environ.get("UPLOAD_BUCKET", "uploads-bucket")
AWS_ENDPOINT_URL = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=AWS_ENDPOINT_URL,
)


def handler(event, context):
    # event is expected to be a dict:
    # {
    #   "fileName": "name.ext",
    #   "contentType": "mime/type",
    #   "fileContent": "<base64>",
    #   "metadata": { ... }
    # }
    try:
        if isinstance(event, str):
            event = json.loads(event)

        file_name = event["fileName"]
        content_type = event.get("contentType", "application/octet-stream")
        file_content_b64 = event["fileContent"]
        metadata = event.get("metadata", {}) or {}

        data = base64.b64decode(file_content_b64)

        s3.put_object(
            Bucket=BUCKET,
            Key=file_name,
            Body=data,
            ContentType=content_type,
            Metadata={k: str(v) for k, v in metadata.items()},
        )

        body = {
            "message": "File stored in S3",
            "bucket": BUCKET,
            "key": file_name,
            "metadata": metadata,
        }

        return {
            "statusCode": 201,
            "body": json.dumps(body),
        }

    except Exception as exc:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(exc)}),
        }
