import requests
import time
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from django.utils import timezone
from music.models import Song, Artist, Album, Platform
from crawler.models import CrawlLog
import logging

logger = logging.getLogger('crawler')


class BaseMusicSpider:
    """音乐爬虫基础类"""
    
    def __init__(self, task):
        self.task = task
        self.platform = task.platform
        self.session = requests.Session()
        self.ua = UserAgent()
        self.setup_session()
        
    def setup_session(self):
        """设置请求会话"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session.headers.update(headers)
        
    def log(self, level, message):
        """记录日志"""
        CrawlLog.objects.create(
            task=self.task,
            level=level,
            message=message
        )
        getattr(logger, level.lower())(f'Task {self.task.id}: {message}')
        
    def get_page(self, url, params=None):
        """获取页面内容"""
        try:
            # 添加随机延迟
            time.sleep(random.uniform(1, self.task.delay_seconds))
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            self.log('DEBUG', f'成功获取页面: {url}')
            return response
            
        except Exception as e:
            self.log('ERROR', f'获取页面失败 {url}: {str(e)}')
            return None
    
    def parse_page(self, response):
        """解析页面内容"""
        if not response:
            return None
        return BeautifulSoup(response.text, 'lxml')
    
    def save_artist(self, artist_data):
        """保存艺术家信息"""
        try:
            artist, created = Artist.objects.get_or_create(
                platform=self.platform,
                platform_id=artist_data['platform_id'],
                defaults={
                    'name': artist_data['name'],
                    'biography': artist_data.get('biography', ''),
                    'platform_url': artist_data.get('platform_url', ''),
                }
            )
            
            if created:
                self.log('INFO', f'新增艺术家: {artist.name}')
            else:
                # 更新信息
                artist.name = artist_data['name']
                artist.biography = artist_data.get('biography', artist.biography)
                artist.platform_url = artist_data.get('platform_url', artist.platform_url)
                artist.save()
                
            return artist
            
        except Exception as e:
            self.log('ERROR', f'保存艺术家失败: {str(e)}')
            return None
    
    def save_album(self, album_data, artist):
        """保存专辑信息"""
        try:
            album, created = Album.objects.get_or_create(
                platform=self.platform,
                platform_id=album_data['platform_id'],
                defaults={
                    'title': album_data['title'],
                    'artist': artist,
                    'description': album_data.get('description', ''),
                    'platform_url': album_data.get('platform_url', ''),
                    'release_date': album_data.get('release_date'),
                }
            )
            
            if created:
                self.log('INFO', f'新增专辑: {album.title}')
            else:
                # 更新信息
                album.title = album_data['title']
                album.description = album_data.get('description', album.description)
                album.platform_url = album_data.get('platform_url', album.platform_url)
                album.save()
                
            return album
            
        except Exception as e:
            self.log('ERROR', f'保存专辑失败: {str(e)}')
            return None
    
    def save_song(self, song_data, artist, album=None):
        """保存歌曲信息"""
        try:
            song, created = Song.objects.get_or_create(
                platform=self.platform,
                platform_id=song_data['platform_id'],
                defaults={
                    'title': song_data['title'],
                    'artist': artist,
                    'album': album,
                    'duration': song_data.get('duration'),
                    'lyrics': song_data.get('lyrics', ''),
                    'genre': song_data.get('genre', ''),
                    'platform_url': song_data.get('platform_url', ''),
                    'audio_url': song_data.get('audio_url', ''),
                    'play_count': song_data.get('play_count', 0),
                    'like_count': song_data.get('like_count', 0),
                }
            )
            
            if created:
                self.log('INFO', f'新增歌曲: {song.title} - {artist.name}')
            else:
                # 更新信息
                song.title = song_data['title']
                song.duration = song_data.get('duration', song.duration)
                song.lyrics = song_data.get('lyrics', song.lyrics)
                song.genre = song_data.get('genre', song.genre)
                song.platform_url = song_data.get('platform_url', song.platform_url)
                song.audio_url = song_data.get('audio_url', song.audio_url)
                song.play_count = song_data.get('play_count', song.play_count)
                song.like_count = song_data.get('like_count', song.like_count)
                song.save()
                
            return song
            
        except Exception as e:
            self.log('ERROR', f'保存歌曲失败: {str(e)}')
            return None
    
    def update_progress(self, current, total):
        """更新任务进度"""
        progress = int((current / total) * 100) if total > 0 else 0
        self.task.progress = progress
        self.task.save()
        
    def crawl(self):
        """爬取方法，子类需要实现"""
        raise NotImplementedError("子类必须实现crawl方法")


def get_spider_by_platform(platform_name):
    """根据平台名称获取对应的爬虫类"""
    spider_map = {
        '网易云音乐': 'crawler.spiders.netease.NeteaseSpider',
        'QQ音乐': 'crawler.spiders.qq.QQMusicSpider',
        '酷狗音乐': 'crawler.spiders.kugou.KugouSpider',
        # 可以继续添加其他平台
    }
    
    spider_path = spider_map.get(platform_name)
    if not spider_path:
        return None
    
    try:
        module_path, class_name = spider_path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[class_name])
        return getattr(module, class_name)
    except ImportError:
        return None