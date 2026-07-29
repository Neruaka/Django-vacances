from django.contrib import admin

from .models import Destination, TravelWish


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("city", "country", "continent", "average_budget", "created_at")
    list_filter = ("continent", "country")
    search_fields = ("city", "country")


@admin.register(TravelWish)
class TravelWishAdmin(admin.ModelAdmin):
    list_display = ("user", "destination", "priority", "visited", "created_at")
    list_filter = ("priority", "visited", "destination__continent")
    search_fields = ("user__username", "destination__city", "destination__country")
