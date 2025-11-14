#!/bin/bash
set -euo pipefail

echo "=== LocalStack init: creating S3 bucket and Lambda function ==="

LAMBDA_ZIP="/tmp/file-upload-lambda.zip"

cd /opt/lambda
zip -r "${LAMBDA_ZIP}" . >/dev/null

awslocal s3 mb s3://uploads-bucket || true

awslocal lambda create-function \
  --function-name file-upload-lambda \
  --runtime python3.11 \
  --zip-file "fileb://${LAMBDA_ZIP}" \
  --handler lambda_function.handler \
  --role arn:aws:iam::000000000000:role/lambda-execution-role \
  --timeout 30 \
  --memory-size 256 \
  --environment "Variables={UPLOAD_BUCKET=uploads-bucket,AWS_REGION=us-east-1,AWS_ENDPOINT_URL=http://localhost:4566}" || true

echo "=== LocalStack init done ==="
