from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status

from app.services.data_processing import read_csv, preprocess_data
from app.services.linear_regression import train_lr_model

model_router = APIRouter()


class TrainModelRequestBody(BaseModel):
    file_name: str
    test_data_percentage: float = 0.7


class PredictRequestBody(BaseModel):
    value: float


@model_router.post("/train_model")
async def train_model_endpoint(body: TrainModelRequestBody):
    try:
        dataset = preprocess_data(read_csv(body.file_name))
        model, mse, rmse, mean_cv_score = train_lr_model(dataset, body.test_data_percentage)

        return {
            "message": "Model trained successfully",
            "data": {
                "mse": mse,
                "rmse": rmse,
                "mean_cv_score": mean_cv_score
            }
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error training the model. {str(e)}")
