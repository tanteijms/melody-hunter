from django.core.management.base import BaseCommand
from crawler.models import CrawlTask
from crawler.tasks import start_crawl_task
from music.models import Platform


class Command(BaseCommand):
    help = '创建并启动音乐爬虫任务'

    def add_arguments(self, parser):
        parser.add_argument('--platform', type=str, required=True, help='音乐平台名称')
        parser.add_argument('--type', type=str, required=True, 
                          choices=['search', 'artist', 'album', 'playlist'],
                          help='爬虫任务类型')
        parser.add_argument('--keyword', type=str, help='搜索关键词（搜索类型必需）')
        parser.add_argument('--url', type=str, help='目标URL（非搜索类型必需）')
        parser.add_argument('--pages', type=int, default=1, help='最大爬取页数')
        parser.add_argument('--delay', type=int, default=1, help='请求延迟秒数')

    def handle(self, *args, **options):
        try:
            # 获取平台
            platform = Platform.objects.get(name=options['platform'])
        except Platform.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'平台 "{options["platform"]}" 不存在')
            )
            return

        # 验证参数
        if options['type'] == 'search' and not options['keyword']:
            self.stdout.write(
                self.style.ERROR('搜索类型任务需要提供关键词')
            )
            return

        if options['type'] != 'search' and not options['url']:
            self.stdout.write(
                self.style.ERROR('非搜索类型任务需要提供目标URL')
            )
            return

        # 创建任务
        task_name = f"{options['type']}-{options['keyword'] or 'url'}-{platform.name}"
        
        task = CrawlTask.objects.create(
            name=task_name,
            platform=platform,
            task_type=options['type'],
            target_url=options.get('url', ''),
            search_keyword=options.get('keyword', ''),
            max_pages=options['pages'],
            delay_seconds=options['delay']
        )

        self.stdout.write(
            self.style.SUCCESS(f'已创建爬虫任务: {task.name} (ID: {task.id})')
        )

        # 启动任务
        start_crawl_task.delay(task.id)
        self.stdout.write(
            self.style.SUCCESS('任务已提交到队列，正在后台执行...')
        )