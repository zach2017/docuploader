# File Upload via AWS Lambda to S3 using LocalStack & Docker Compose

This example shows how to:

- Run **LocalStack** with S3 + Lambda using Docker Compose  
- Expose a **FastAPI** HTTP endpoint that receives a file + metadata  
- Invoke a **Python AWS Lambda** which writes the file to **S3** (in LocalStack)

## Architecture

1. Client uploads file (multipart) + metadata to `POST /api/files/upload`
2. FastAPI service calls `file-upload-lambda` via AWS Lambda API (LocalStack endpoint)
3. Lambda decodes the file, writes it to S3 bucket `uploads-bucket` with metadata
4. Response returns S3 bucket/key + metadata

## Prereqs

- Docker + Docker Compose

## How to Run

```bash
docker compose up --build
```

> Note: You may need to mark the init script as executable on your host:

```bash
chmod +x init-scripts/01-setup.sh
docker compose up --build
```

This will:

- Start LocalStack on `http://localhost:4566`
- Create S3 bucket `uploads-bucket`
- Package and deploy Lambda `file-upload-lambda`
- Start FastAPI on `http://localhost:8000`

## Test the Upload

```bash
curl -X POST "http://localhost:8000/api/files/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/local/file.pdf" \
  -F 'metadata={\"documentType\":\"invoice\",\"owner\":\"zac\"}'
```

Example JSON response:

```json
{
  "statusCode": 201,
  "body": {
    "message": "File stored in S3",
    "bucket": "uploads-bucket",
    "key": "file.pdf",
    "metadata": {
      "documentType": "invoice",
      "owner": "zac"
    }
  }
}
```

## Inspect S3 (via LocalStack)

From inside the LocalStack container:

```bash
docker exec -it localstack awslocal s3 ls s3://uploads-bucket
```

You should see your uploaded file listed there.
