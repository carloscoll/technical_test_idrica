import pandas as pd


def upload_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer='data/' + name + '.csv',
                       sep=",",
                       parse_dates=['timestamp'],
                       na_values="null",
                       converters={
                           'sensor_a': lambda x: pd.to_numeric(x.strip(), errors='coerce'),
                           'sensor_b': lambda x: pd.to_numeric(x.strip(), errors='coerce')
                       })


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df['sensor_a'] = df['sensor_a'].fillna(df['sensor_a'].expanding().mean())
    df['sensor_b'] = df['sensor_b'].fillna(df['sensor_b'].expanding().mean())

    df['sensor_a'] = df['sensor_a'].apply(lambda x: max(4, min(x, 7.5)))

    df['sensor_b'] = df['sensor_b'].apply(lambda x: max(5000, min(x, 7500)))

    return df
