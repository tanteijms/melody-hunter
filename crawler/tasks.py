from celery import shared_task
from django.utils import timezone
from .models import CrawlTask, CrawlLog
from .spiders.base import get_spider_by_platform
import logging

logger = logging.getLogger('crawler')


@shared_task
def start_crawl_task(task_id):
    """启动爬虫任务"""
    try:
        task = CrawlTask.objects.get(id=task_id)
        task.status = 'running'
        task.started_at = timezone.now()
        task.save()
        
        # 记录日志
        CrawlLog.objects.create(
            task=task,
            level='INFO',
            message=f'开始执行爬虫任务: {task.name}'
        )
        
        # 根据平台获取对应的爬虫
        spider_class = get_spider_by_platform(task.platform.name)
        if not spider_class:
            raise Exception(f'不支持的平台: {task.platform.name}')
        
        # 初始化爬虫
        spider = spider_class(task)
        
        # 执行爬虫
        result = spider.crawl()
        
        # 更新任务状态
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.progress = 100
        task.total_found = result.get('found', 0)
        task.total_saved = result.get('saved', 0)
        task.total_failed = result.get('failed', 0)
        task.save()
        
        CrawlLog.objects.create(
            task=task,
            level='INFO',
            message=f'任务完成: 发现{task.total_found}项，保存{task.total_saved}项，失败{task.total_failed}项'
        )
        
    except Exception as e:
        # 更新任务状态为失败
        task.status = 'failed'
        task.completed_at = timezone.now()
        task.save()
        
        CrawlLog.objects.create(
            task=task,
            level='ERROR',
            message=f'任务执行失败: {str(e)}'
        )
        
        logger.error(f'爬虫任务失败 {task_id}: {str(e)}')
        raise