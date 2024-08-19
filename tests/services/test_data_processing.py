import pandas as pd

from app.services.data_processing import preprocess_data, read_csv


def test_upload_csv_valid_file(mocker):
    mock_csv_data = """timestamp,sensor_a,sensor_b
                       2023-01-01T12:00:00,5.828125,6313.940244
                       2023-01-01T12:01:00,6.584896,5931.038263
                       2023-01-01T12:02:00,6.847396,5672.298411
                       2023-01-01T12:03:00,null,5639.848733"""

    mocker.patch('builtins.open', mocker.mock_open(read_data=mock_csv_data))
    df = read_csv('mock_file')

    assert df['sensor_a'].dtype == 'float64'
    assert df['sensor_b'].dtype == 'float64'
    assert df['timestamp'].dtype == 'datetime64[ns]'

    assert pd.isna(df['sensor_a'].iloc[3])


def test_upload_csv_invalid_values(mocker):
    mock_csv_data = """timestamp,sensor_a,sensor_b
                       2023-01-01T12:00:00,5.828125,abc
                       2023-01-01T12:01:00,null,5931.038263"""

    mocker.patch('builtins.open', mocker.mock_open(read_data=mock_csv_data))
    df = read_csv('mock_file')

    assert pd.isna(df['sensor_b'].iloc[0])
    assert pd.isna(df['sensor_a'].iloc[1])


def test_preprocess_data_nan_filled_correctly():
    data = {
        'sensor_a': [5.0, 6.0, None, 7.5, None],
        'sensor_b': [6000, 7000, 7500, None, 5000]
    }
    df = pd.DataFrame(data)

    df_processed = preprocess_data(df)

    assert df_processed['sensor_a'].iloc[2] == (5.0 + 6.0) / 2
    assert df_processed['sensor_b'].iloc[3] == (6000 + 7000 + 7500) / 3


def test_preprocess_data_clipping():
    data = {
        'sensor_a': [3.0, 8.0, 6.0],
        'sensor_b': [4000, 8000, 7000]
    }
    df = pd.DataFrame(data)

    df_processed = preprocess_data(df)

    assert df_processed['sensor_a'].iloc[0] == 4.0
    assert df_processed['sensor_a'].iloc[1] == 7.5
    assert df_processed['sensor_b'].iloc[0] == 5000
    assert df_processed['sensor_b'].iloc[1] == 7500
