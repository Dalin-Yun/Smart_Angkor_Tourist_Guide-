from django.contrib import admin
from .models import Temple, Road


@admin.register(Temple)
class TempleAdmin(admin.ModelAdmin):
    list_display = ("temple_id", "name", "category", "rating", "visit_time")
    search_fields = ("name", "temple_id")
    list_filter = ("category",)


@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance")
