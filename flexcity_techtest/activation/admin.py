import datetime

from django.contrib import admin
from .models import Asset, Availability


# Register your models here.
class AvailabilityInline(admin.TabularInline):
    model = Availability


@admin.action(description="Make selected assets available today")
def activate_assets(modeladmin, request, queryset):
    today = datetime.date.today()
    for asset in queryset:
        Availability.objects.get_or_create(asset=asset, date=today)


class AssetAdmin(admin.ModelAdmin):
    inlines = [AvailabilityInline]
    actions = [activate_assets]


admin.site.register(Asset, AssetAdmin)
