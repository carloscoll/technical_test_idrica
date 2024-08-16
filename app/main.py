from fastapi import FastAPI
from app.routers.csv_upload_router import csv_upload_router

app = FastAPI()

app.include_router(csv_upload_router, tags=["CSV Upload"])
