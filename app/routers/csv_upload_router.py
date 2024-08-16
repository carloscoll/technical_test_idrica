from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status

from app.services.data_processing import upload_csv

csv_upload_router = APIRouter()


class FileUploadRequestBody(BaseModel):
    file_name: str


@csv_upload_router.post("/upload")
async def upload_csv_endpoint(body: FileUploadRequestBody):
    try:
        df = upload_csv(body.file_name)
        data_head = df.head().to_dict()

        return {
            "message": "File uploaded successfully",
            "data": data_head
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error processing file: {str(e)}")
