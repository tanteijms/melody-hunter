from rest_framework import serializers
from .models import CrawlTask, CrawlLog


class CrawlLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlLog
        fields = '__all__'


class CrawlTaskSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    duration = serializers.CharField(read_only=True)
    logs = CrawlLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = CrawlTask
        fields = ['id', 'name', 'platform', 'platform_name', 'task_type', 
                 'target_url', 'search_keyword', 'status', 'progress', 
                 'max_pages', 'delay_seconds', 'total_found', 'total_saved', 
                 'total_failed', 'started_at', 'completed_at', 'created_at', 
                 'updated_at', 'duration', 'logs']


class CreateCrawlTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlTask
        fields = ['name', 'platform', 'task_type', 'target_url', 
                 'search_keyword', 'max_pages', 'delay_seconds']