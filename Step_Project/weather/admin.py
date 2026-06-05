from django.contrib import admin

from .models import (
    Weather,
    SearchHistory,
)

admin.site.register(Weather)
admin.site.register(SearchHistory)
