import pandas as pd

from app.services.linear_regression import predict, train_lr_model


def test_model_training():
    data = {
        'sensor_a': [5.0, 6.0, 4.0, 7.5, 5.5],
        'sensor_b': [6000, 7000, 7500, 6500, 5000]
    }
    df = pd.DataFrame(data)
    model, _, _, _ = train_lr_model(df)

    assert len(model.coef_) == 1
    assert model.intercept_ is not None


def test_prediction_function():
    data = {
        'sensor_a': [5.0, 6.0, 4.0, 7.5, 5.5],
        'sensor_b': [6000, 7000, 7500, 6500, 5000]
    }
    df = pd.DataFrame(data)
    model, _, _, _ = train_lr_model(df)

    sensor_b_value = 6500
    predicted_value = predict(sensor_b_value)

    assert 4.0 <= predicted_value['value'] <= 7.5
