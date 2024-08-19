from fastapi import FastAPI

from app.routers.csv_upload_router import csv_upload_router
from app.routers.model_router import model_router
from app.utils.database import initialize_db

app = FastAPI()

app.include_router(csv_upload_router, tags=["CSV upload endpoints"])
app.include_router(model_router, tags=["Linear regression model endpoints"])

initialize_db()
