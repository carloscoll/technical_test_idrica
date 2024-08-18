from fastapi import FastAPI

from app.routers.csv_upload_router import csv_upload_router
from app.utils.database import initialize_db

app = FastAPI()

app.include_router(csv_upload_router, tags=["CSV Upload"])

initialize_db()
