from typing import List

from ..schemas import ActivationIn, AssetSchema
from ..models import Asset, Availability

from django.conf import settings
import logging

from .knapsack_solver import get_assets_knapsack_solver
from .greedy import get_assets_greedy


def get_activated_assets(data: ActivationIn, strategy: str = None) -> List[AssetSchema]:

    activable_assets = Asset.objects.filter(
        availability__in=Availability.objects.filter(date=data.date)
    )

    available_capacity = sum([asset.volume for asset in activable_assets])

    if available_capacity < data.volume:
        raise Exception("Not enough capacity available")
    
    logging.info(f"Activating {data.volume} volume for date {data.date}")

    strategy = strategy or settings.DEFAULT_STRATEGY
    ## select strategy
    match strategy:
        case "all":
            activated_assets = activable_assets

        case "greedy":
            activated_assets = get_assets_greedy(activable_assets, data.volume)

        case "knapsack_solver":
            activated_assets = get_assets_knapsack_solver(activable_assets, data.volume)

    logging.info(
        f"Activated {len(activated_assets)} assets with total capacity {sum([asset.volume for asset in activated_assets])} \
and total cost {sum([asset.activation_cost for asset in activated_assets])} using strategy {strategy}"
    )

    return activated_assets
