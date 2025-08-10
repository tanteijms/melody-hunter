from django.contrib import admin
from .models import CrawlTask, CrawlLog


@admin.register(CrawlTask)
class CrawlTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'task_type', 'status', 'created_at', 'updated_at']
    list_filter = ['platform', 'task_type', 'status', 'created_at']
    search_fields = ['name', 'target_url']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CrawlLog)
class CrawlLogAdmin(admin.ModelAdmin):
    list_display = ['task', 'level', 'message', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['message']
    readonly_fields = ['created_at']