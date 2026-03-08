from ninja import Schema, ModelSchema
import datetime
from .models import Asset


class ActivationIn(Schema):
    date: datetime.date
    volume: int


class AssetSchema(ModelSchema):
    class Meta:
        model = Asset
        fields = ["code", "name", "activation_cost", "volume"]


class ErrorSchema(Schema):
    error: str
