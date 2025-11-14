from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import boto3
import os
import base64
import json

app = FastAPI(title="File Upload via Lambda to S3 (LocalStack)", version="1.0.0")

AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localstack:4566")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
LAMBDA_NAME = os.getenv("UPLOAD_LAMBDA_NAME", "file-upload-lambda")

lambda_client = boto3.client(
    "lambda",
    region_name=AWS_REGION,
    endpoint_url=AWS_ENDPOINT_URL,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
)


@app.post("/api/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")

    metadata_obj = {}
    if metadata:
        try:
            metadata_obj = json.loads(metadata)
        except json.JSONDecodeError:
            metadata_obj = {"raw": metadata}

    payload = {
        "fileName": file.filename,
        "contentType": file.content_type,
        "fileContent": base64.b64encode(content).decode("utf-8"),
        "metadata": metadata_obj,
    }

    try:
        response = lambda_client.invoke(
            FunctionName=LAMBDA_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload).encode("utf-8"),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error invoking lambda: {exc}")

    raw_payload = response.get("Payload").read()
    try:
        lambda_result = json.loads(raw_payload)
    except Exception:
        lambda_result = {"raw": raw_payload.decode("utf-8")}

    body_raw = lambda_result.get("body")
    body = None
    if isinstance(body_raw, str):
        try:
            body = json.loads(body_raw)
        except Exception:
            body = body_raw
    else:
        body = body_raw

    result = {
        "statusCode": lambda_result.get("statusCode", 201),
        "body": body,
    }

    return JSONResponse(
        status_code=result["statusCode"],
        content=result,
    )
