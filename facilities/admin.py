from django.contrib import admin
from .models import Facility


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "town", "phone", "fax", "unit_private", "unit_multi",
                    "traditional_private", "traditional_multi", "capacity")
    list_filter = ("region", "unit_private", "unit_multi",
                   "traditional_private", "traditional_multi")
    search_fields = ("name", "address")
