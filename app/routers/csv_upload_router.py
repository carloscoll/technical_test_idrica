import os

from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette import status

from app.services.data_processing import upload_csv

csv_upload_router = APIRouter()


@csv_upload_router.post("/upload")
async def upload_csv_endpoint(file: UploadFile = File(...)):
    try:
        file_path = upload_csv(file)
        filename = os.path.basename(file_path)
        return {
            "message": f"File '{filename}' uploaded successfully",
            "file_path": file_path
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error processing file: {str(e)}")
