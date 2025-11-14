from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from typing import Optional
import json
import os

from .config import config

app = FastAPI(title="Python File Upload API", version="1.0.0")

# Ensure upload directory exists
os.makedirs(config.storage.base_path, exist_ok=True)

@app.post("/api/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
):
    if file is None:
        raise HTTPException(status_code=400, detail="File is required")

    original_filename = file.filename or "uploaded-file"
    suffix = Path(original_filename).suffix
    stored_name = f"{uuid4()}_{int(datetime.utcnow().timestamp()*1000)}{suffix}"

    target_path = config.storage.base_path / stored_name

    try:
        # Save file to disk
        with target_path.open("wb") as f_out:
            while True:
                chunk = await file.read(8192)
                if not chunk:
                    break
                f_out.write(chunk)

        # Save metadata as sidecar JSON file if present
        metadata_obj = None
        if metadata:
            try:
                metadata_obj = json.loads(metadata)
            except json.JSONDecodeError:
                # keep original string if not valid json
                metadata_obj = {"raw": metadata}

            meta_path = config.storage.base_path / f"{stored_name}.meta.json"
            with meta_path.open("w", encoding="utf-8") as mf:
                json.dump(metadata_obj, mf, indent=2)

        return JSONResponse(
            status_code=201,
            content={
                "fileName": stored_name,
                "originalFileName": original_filename,
                "contentType": file.content_type,
                "size": target_path.stat().st_size,
                "metadata": metadata_obj,
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not store file: {exc}")
