from django.db import models
from django.utils import timezone


class CrawlTask(models.Model):
    """爬虫任务模型"""
    
    STATUS_CHOICES = [
        ('pending', '等待中'),
        ('running', '运行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
        ('cancelled', '已取消'),
    ]
    
    TYPE_CHOICES = [
        ('search', '搜索爬取'),
        ('artist', '艺术家爬取'),
        ('album', '专辑爬取'),
        ('playlist', '歌单爬取'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='任务名称')
    platform = models.ForeignKey('music.Platform', on_delete=models.CASCADE, verbose_name='目标平台')
    task_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='任务类型')
    target_url = models.URLField(verbose_name='目标URL')
    search_keyword = models.CharField(max_length=200, blank=True, verbose_name='搜索关键词')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    progress = models.PositiveIntegerField(default=0, verbose_name='进度百分比')
    
    # 爬取配置
    max_pages = models.PositiveIntegerField(default=1, verbose_name='最大页数')
    delay_seconds = models.PositiveIntegerField(default=1, verbose_name='延迟秒数')
    
    # 结果统计
    total_found = models.PositiveIntegerField(default=0, verbose_name='发现总数')
    total_saved = models.PositiveIntegerField(default=0, verbose_name='保存总数')
    total_failed = models.PositiveIntegerField(default=0, verbose_name='失败总数')
    
    # 时间字段
    started_at = models.DateTimeField(blank=True, null=True, verbose_name='开始时间')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '爬虫任务'
        verbose_name_plural = '爬虫任务'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} ({self.platform.name})"
    
    def duration(self):
        """计算任务持续时间"""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        elif self.started_at:
            return timezone.now() - self.started_at
        return None


class CrawlLog(models.Model):
    """爬虫日志模型"""
    
    LEVEL_CHOICES = [
        ('DEBUG', '调试'),
        ('INFO', '信息'),
        ('WARNING', '警告'),
        ('ERROR', '错误'),
        ('CRITICAL', '严重'),
    ]
    
    task = models.ForeignKey(CrawlTask, on_delete=models.CASCADE, related_name='logs', verbose_name='关联任务')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name='日志级别')
    message = models.TextField(verbose_name='日志信息')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '爬虫日志'
        verbose_name_plural = '爬虫日志'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.level}: {self.message[:50]}"