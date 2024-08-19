import io

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_upload_csv(mocker):
    return mocker.patch('app.routers.csv_upload_router.upload_csv', return_value="data/test_data.csv")


def test_upload_csv_success(mock_upload_csv):
    file_content = b"timestamp,sensor_a,sensor_b\n2023-01-01T12:00:00,5.828125,6313.940244\n"
    file_like = io.BytesIO(file_content)
    file_like.name = "test_data.csv"

    response = client.post("/upload", files={"file": (file_like.name, file_like, "text/csv")})

    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "File 'test_data.csv' uploaded successfully"
    assert "file_path" in response.json()
    assert response.json()["file_path"] == "data/test_data.csv"


def test_upload_csv_failure(mocker):
    mocker.patch('app.routers.csv_upload_router.upload_csv', side_effect=Exception("Error processing file"))

    file_content = b"timestamp,sensor_a,sensor_b\n2023-01-01T12:00:00,5.828125,6313.940244\n"
    file_like = io.BytesIO(file_content)
    file_like.name = "test_data.csv"

    response = client.post("/upload", files={"file": (file_like.name, file_like, "text/csv")})

    assert response.status_code == 400
    assert "detail" in response.json()
