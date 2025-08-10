from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import CrawlTask, CrawlLog
from .serializers import CrawlTaskSerializer, CreateCrawlTaskSerializer, CrawlLogSerializer
from .tasks import start_crawl_task


class CrawlTaskViewSet(viewsets.ModelViewSet):
    """爬虫任务视图集"""
    queryset = CrawlTask.objects.select_related('platform').all()
    serializer_class = CrawlTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform', 'task_type', 'status']
    search_fields = ['name', 'search_keyword']
    ordering_fields = ['created_at', 'updated_at', 'started_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCrawlTaskSerializer
        return CrawlTaskSerializer
    
    def perform_create(self, serializer):
        """创建任务时自动启动"""
        task = serializer.save()
        # 启动异步爬虫任务
        start_crawl_task.delay(task.id)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """手动启动任务"""
        task = self.get_object()
        if task.status == 'pending':
            start_crawl_task.delay(task.id)
            return Response({'message': '任务已启动'})
        else:
            return Response({'error': '任务状态不允许启动'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消任务"""
        task = self.get_object()
        if task.status in ['pending', 'running']:
            task.status = 'cancelled'
            task.save()
            return Response({'message': '任务已取消'})
        else:
            return Response({'error': '任务状态不允许取消'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取统计信息"""
        stats = {
            'total': self.queryset.count(),
            'pending': self.queryset.filter(status='pending').count(),
            'running': self.queryset.filter(status='running').count(),
            'completed': self.queryset.filter(status='completed').count(),
            'failed': self.queryset.filter(status='failed').count(),
            'cancelled': self.queryset.filter(status='cancelled').count(),
        }
        return Response(stats)


class CrawlLogViewSet(viewsets.ReadOnlyModelViewSet):
    """爬虫日志视图集"""
    queryset = CrawlLog.objects.select_related('task').all()
    serializer_class = CrawlLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['task', 'level']
    search_fields = ['message']
    ordering = ['-created_at']