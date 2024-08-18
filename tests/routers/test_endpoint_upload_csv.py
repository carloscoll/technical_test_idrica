import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_upload_csv(mocker):
    mocker.patch('app.routers.csv_upload_router.upload_csv', return_value=pd.DataFrame({
        'timestamp': ['2023-01-01T12:00:00', '2023-01-01T12:01:00', '2023-01-01T12:02:00'],
        'sensor_a': [5.828125, 6.584896, 6.847396],
        'sensor_b': [6313.940244, 5931.038263, 5672.298411]
    }))


def test_upload_csv_success(mock_upload_csv):
    response = client.post("/upload", json={"file_name": "test"})
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "File uploaded successfully"
    assert "data" in response.json()
    assert response.json()["data"] == {
        'timestamp': {'0': '2023-01-01T12:00:00', '1': '2023-01-01T12:01:00', '2': '2023-01-01T12:02:00'},
        'sensor_a': {'0': 5.828125, '1': 6.584896, '2': 6.847396},
        'sensor_b': {'0': 6313.940244, '1': 5931.038263, '2': 5672.298411}
    }


def test_upload_csv_failure(mocker):
    mocker.patch('app.services.data_processing.upload_csv', side_effect=Exception("Error processing file"))
    response = client.post("/upload", json={"file_name": "data1"})
    assert response.status_code == 400
    assert "detail" in response.json()
