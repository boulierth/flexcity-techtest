from ..models import Asset
from django.db.models import Case, QuerySet, F, Value, When


def get_assets_greedy(available_assets: QuerySet[Asset], volume):

    selected_assets = []

    needed_volume = volume

    while needed_volume > 0 and available_assets.exists():

        # if capacity provided is bigger than necessary volume, use rate for the needed volume instead
        available_assets = available_assets.annotate(
            rate=F("activation_cost")
            / Case(
                When(volume__gte=needed_volume, then=Value(needed_volume)),
                default=F("volume"),
            )
        )
        available_assets = available_assets.order_by("rate")

        # pick cheaper asset
        asset = available_assets.first()

        selected_assets.append(asset)

        needed_volume -= asset.volume

        available_assets = available_assets.exclude(id=asset.id)

    # while a selected asset has less volume than the overflow, we can remove the most expensive asset to reduce the cost
    overflow = -needed_volume
    while (
        overflow > 0
        and min(selected_assets, key=lambda asset: asset.volume).volume <= overflow
    ):

        # remove the most expensive asset smaller than the overflow
        removable_assets = [
            asset for asset in selected_assets if asset.volume <= overflow
        ]

        # Q? Should we remove the most expensive asset or the one with the worst rate?
        removable_asset = max(
            removable_assets, key=lambda asset: asset.activation_cost / asset.volume
        )

        selected_assets.remove(removable_asset)
        overflow -= removable_asset.volume

    return selected_assets
