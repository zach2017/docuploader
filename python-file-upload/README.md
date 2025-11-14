# Python File Upload Example (FastAPI)

This is a minimal FastAPI app that uploads a file to a local directory and stores optional JSON metadata alongside it.

## Features

- Reads storage config from `config.yml`:
  - `storage.base_path` for where files are stored
  - `storage.key_info` placeholder for any secret / key info
- POST endpoint: `POST /api/files/upload`
  - `file`: multipart file
  - `metadata`: optional string (JSON recommended)

If `metadata` is valid JSON, it is saved as `<storedFileName>.meta.json`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use values from `config.yml` manually.

## Test with curl

```bash
curl -X POST "http://localhost:8000/api/files/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/local/file.pdf" \
  -F 'metadata={\"documentType\":\"invoice\",\"owner\":\"zac\"}'
```
