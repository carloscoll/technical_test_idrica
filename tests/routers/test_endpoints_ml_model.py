import pandas as pd
import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)


@pytest.fixture
def mock_train_lr_model():
    with patch('app.routers.model_router.train_lr_model') as mock:
        mock.return_value = (MagicMock(), 0.5, 0.7, 0.6)
        yield mock


@pytest.fixture
def mock_predict():
    with patch('app.routers.model_router.predict') as mock:
        mock.return_value = {"predicted_value": 5.67}
        yield mock


@pytest.fixture
def mock_read_csv():
    with patch('app.routers.model_router.read_csv') as mock:
        mock.return_value = pd.DataFrame({
            'timestamp': pd.to_datetime(['2023-01-01T00:00:00', '2023-01-01T01:00:00']),
            'sensor_a': [5.0, 6.0],
            'sensor_b': [6000, 7000]
        })
        yield mock


def test_train_model_success(mock_train_lr_model, mock_read_csv):
    response = client.post(
        "/train_model",
        json={"file_name": "test", "test_data_percentage": 0.7}
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Model trained successfully"
    assert "data" in response.json()
    assert response.json()["data"]["mse"] == 0.5
    assert response.json()["data"]["rmse"] == 0.7
    assert response.json()["data"]["mean_cv_score"] == 0.6


def test_train_model_failure():
    with patch('app.services.data_processing.preprocess_data', side_effect=Exception("Preprocessing error")):
        response = client.post(
            "/train_model",
            json={"file_name": "invalid_file", "test_data_percentage": 0.7}
        )

        assert response.status_code == 400
        assert "Error training the model" in response.json()["detail"]


def test_predict_success(mock_predict):
    response = client.post("/predict", json={"value": 10.0})

    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "New value predicted and stored in the database successfully"
    assert "data" in response.json()
    assert response.json()["data"] == {"predicted_value": 5.67}


def test_predict_failure(mocker):
    mocker.patch('app.routers.model_router.predict', side_effect=Exception("Prediction failed"))

    response = client.post("/predict", json={"value": 10.0})

    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Error predicting a new value. Prediction failed"
