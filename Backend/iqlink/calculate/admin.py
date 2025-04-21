from django.contrib import admin
from .models import KeySet

@admin.register(KeySet)
class KeySetAdmin(admin.ModelAdmin):
    list_display = ('key', 'data')
    search_fields = ('key',)

