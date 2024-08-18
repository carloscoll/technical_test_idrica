import os
import re

import pandas as pd
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, cross_val_score
import joblib

from app.models import Predictions


def train_lr_model(dataset: DataFrame, train_percentage: float = 0.8):
    X = dataset[['sensor_b']]
    y = dataset['sensor_a']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_percentage)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
    mean_cv_score = (-cv_scores).mean()

    save_model_with_incremental_versioning(model)

    print(f"Root Mean Squared Error: {rmse}")
    print(f"Mean Squared Error: {mse}")
    print(f"Cross-Validation MSE: {mean_cv_score}")


def get_latest_version(model_directory="ml_models"):
    model_files = [f for f in os.listdir(model_directory) if re.match(r'linear_regression_model_\d+\.joblib', f)]

    if not model_files:
        return 1

    versions = [int(re.search(r'_(\d+)\.joblib', f).group(1)) for f in model_files]
    return max(versions)


def save_model_with_incremental_versioning(model: LinearRegression, model_directory: str = "ml_models") -> str:
    latest_version = get_latest_version(model_directory)
    new_version = latest_version + 1

    model_filename = f"linear_regression_model_{new_version}.joblib"
    model_path = os.path.join(model_directory, model_filename)

    joblib.dump(model, model_path)

    print(f"Model saved as: {model_path}")
    return model_path


def load_latest_version_model(model_directory: str = "ml_models") -> LinearRegression:
    latest_version = get_latest_version(model_directory)
    if latest_version == 0:
        raise FileNotFoundError("No models in the selected folder.")

    model_filename = f"linear_regression_model_{latest_version}.joblib"
    model_path = os.path.join(model_directory, model_filename)

    model = joblib.load(model_path)
    print(f"Model loaded from: {model_path}")
    return model


def predict(data_point: float) -> Predictions:
    X_new = pd.DataFrame({'sensor_b': [data_point]})
    model = load_latest_version_model()
    value_predicted = model.predict(X_new)
    prediction = Predictions.create(sensor_b=data_point, predicted=value_predicted)

    return prediction
