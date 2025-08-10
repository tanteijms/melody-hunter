from django.core.management.base import BaseCommand
from music.models import Platform


class Command(BaseCommand):
    help = '初始化音乐平台数据'

    def handle(self, *args, **options):
        platforms = [
            {
                'name': '网易云音乐',
                'base_url': 'https://music.163.com',
                'is_active': True
            },
            {
                'name': 'QQ音乐',
                'base_url': 'https://y.qq.com',
                'is_active': True
            },
            {
                'name': '酷狗音乐',
                'base_url': 'https://www.kugou.com',
                'is_active': True
            },
            {
                'name': '酷我音乐',
                'base_url': 'https://www.kuwo.cn',
                'is_active': False  # 暂未实现
            },
            {
                'name': '咪咕音乐',
                'base_url': 'https://www.migu.cn',
                'is_active': False  # 暂未实现
            }
        ]

        created_count = 0
        for platform_data in platforms:
            platform, created = Platform.objects.get_or_create(
                name=platform_data['name'],
                defaults=platform_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'创建平台: {platform.name}')
                )
            else:
                # 更新现有平台信息
                platform.base_url = platform_data['base_url']
                platform.is_active = platform_data['is_active']
                platform.save()
                self.stdout.write(
                    self.style.WARNING(f'更新平台: {platform.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n平台初始化完成! 新建: {created_count}, 总计: {Platform.objects.count()}')
        )