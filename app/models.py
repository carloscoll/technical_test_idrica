import datetime
import uuid

from peewee import Model, UUIDField, DateTimeField, FloatField

from app.utils.database import db


class Predictions(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    sensor_b = FloatField()
    value = FloatField()

    class Meta:
        database = db

    def __init__(self, **data):
        super().__init__(**data)
        sensor_b_data = data['sensor_b']
        sensor_a_data = data['predicted'][0]
        self.value = max(4, min(sensor_a_data, 7.5))
        self.sensor_b = max(5000, min(sensor_b_data, 7500))
