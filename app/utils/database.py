import os

from peewee import SqliteDatabase

db_directory = 'db'
os.makedirs(db_directory, exist_ok=True)

db_path = os.path.join(db_directory, 'predictions.db')

db = SqliteDatabase(db_path)


def initialize_db():
    db.connect()
    from app.models import Predictions
    db.create_tables([Predictions])
