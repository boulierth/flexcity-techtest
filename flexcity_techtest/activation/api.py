from datetime import datetime, timedelta
from typing import List
from ninja import NinjaAPI
from ninja.errors import HttpError
from .schemas import ActivationIn, AssetSchema, ErrorSchema
from .models import Asset, Availability
import re

from .business.strategy import get_activated_assets

api = NinjaAPI()


@api.post("/activate", response=List[AssetSchema] | ErrorSchema)
def activate(request, data: ActivationIn, policy: str = None):

    try:
        activated_assets = get_activated_assets(data, policy)
    except Exception as e:
        return {"error": str(e)}
    return activated_assets


@api.get("/available-capacity", response=dict)
def available_assets(request, date: str = None):
    if not date:
        available_assets = Asset.objects.all()
    else:
        match date:
            case "today":
                converted_date = datetime.today().date()
            case "tomorrow":
                converted_date = datetime.today().date() + timedelta(days=1)
            case str() as d if (pattern := r"\d{4}-\d{2}-\d{2}") and re.fullmatch(pattern, d):
                converted_date = datetime.strptime(d, "%Y-%m-%d").date()
            case _:
                raise HttpError(400, "Invalid date format. Use YYYY-MM-DD.")

        available_assets = Asset.objects.filter(
            availability__in=Availability.objects.filter(date=converted_date)
        )

    return {
        "total_capacity": sum([asset.volume for asset in available_assets]),
        "total_cost": sum([asset.activation_cost for asset in available_assets]),
    }
