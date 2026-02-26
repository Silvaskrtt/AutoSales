from django.contrib import admin
from .models import Dashboard


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
	list_display = ("title", "owner", "is_public", "updated_at")
	search_fields = ("title", "description")
	prepopulated_fields = {"slug": ("title",)}
	list_filter = ("is_public",)
