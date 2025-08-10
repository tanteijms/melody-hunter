import re
import json
from .base import BaseMusicSpider


class NeteaseSpider(BaseMusicSpider):
    """网易云音乐爬虫"""
    
    def __init__(self, task):
        super().__init__(task)
        self.base_url = 'https://music.163.com'
        
    def crawl(self):
        """执行爬取任务"""
        self.log('INFO', f'开始爬取网易云音乐，任务类型: {self.task.task_type}')
        
        result = {
            'found': 0,
            'saved': 0,
            'failed': 0
        }
        
        try:
            if self.task.task_type == 'search':
                result = self.crawl_search()
            elif self.task.task_type == 'artist':
                result = self.crawl_artist()
            elif self.task.task_type == 'album':
                result = self.crawl_album()
            elif self.task.task_type == 'playlist':
                result = self.crawl_playlist()
            else:
                raise ValueError(f'不支持的任务类型: {self.task.task_type}')
                
        except Exception as e:
            self.log('ERROR', f'爬取过程中发生错误: {str(e)}')
            result['failed'] += 1
            
        return result
    
    def crawl_search(self):
        """搜索爬取"""
        keyword = self.task.search_keyword
        if not keyword:
            raise ValueError('搜索任务需要提供关键词')
            
        self.log('INFO', f'开始搜索: {keyword}')
        
        # 这里是示例实现，实际需要根据网易云音乐的API进行调整
        search_url = f'{self.base_url}/api/search/get/web'
        
        result = {'found': 0, 'saved': 0, 'failed': 0}
        
        for page in range(1, self.task.max_pages + 1):
            params = {
                's': keyword,
                'type': 1,  # 1表示单曲
                'offset': (page - 1) * 30,
                'limit': 30
            }
            
            response = self.get_page(search_url, params)
            if not response:
                result['failed'] += 1
                continue
                
            try:
                data = response.json()
                songs = data.get('result', {}).get('songs', [])
                
                result['found'] += len(songs)
                
                for song_info in songs:
                    if self.parse_and_save_song(song_info):
                        result['saved'] += 1
                    else:
                        result['failed'] += 1
                        
                self.update_progress(page, self.task.max_pages)
                
            except Exception as e:
                self.log('ERROR', f'解析搜索结果失败: {str(e)}')
                result['failed'] += 1
                
        return result
    
    def crawl_artist(self):
        """艺术家页面爬取"""
        # 从目标URL中提取艺术家ID
        artist_id = self.extract_artist_id(self.task.target_url)
        if not artist_id:
            raise ValueError('无法从URL中提取艺术家ID')
            
        self.log('INFO', f'开始爬取艺术家: {artist_id}')
        
        # 实现艺术家信息爬取逻辑
        result = {'found': 0, 'saved': 0, 'failed': 0}
        
        # 这里添加具体的艺术家爬取逻辑
        
        return result
    
    def crawl_album(self):
        """专辑页面爬取"""
        # 实现专辑爬取逻辑
        result = {'found': 0, 'saved': 0, 'failed': 0}
        return result
    
    def crawl_playlist(self):
        """歌单页面爬取"""
        # 实现歌单爬取逻辑
        result = {'found': 0, 'saved': 0, 'failed': 0}
        return result
    
    def extract_artist_id(self, url):
        """从URL中提取艺术家ID"""
        match = re.search(r'artist\?id=(\d+)', url)
        return match.group(1) if match else None
    
    def parse_and_save_song(self, song_info):
        """解析并保存歌曲信息"""
        try:
            # 解析艺术家信息
            artist_info = song_info.get('artists', [{}])[0]
            artist_data = {
                'name': artist_info.get('name', ''),
                'platform_id': str(artist_info.get('id', '')),
                'platform_url': f'{self.base_url}/artist?id={artist_info.get("id", "")}'
            }
            
            artist = self.save_artist(artist_data)
            if not artist:
                return False
            
            # 解析专辑信息
            album_info = song_info.get('album', {})
            album = None
            if album_info:
                album_data = {
                    'title': album_info.get('name', ''),
                    'platform_id': str(album_info.get('id', '')),
                    'platform_url': f'{self.base_url}/album?id={album_info.get("id", "")}'
                }
                album = self.save_album(album_data, artist)
            
            # 解析歌曲信息
            song_data = {
                'title': song_info.get('name', ''),
                'platform_id': str(song_info.get('id', '')),
                'duration': song_info.get('duration', 0) // 1000,  # 毫秒转秒
                'platform_url': f'{self.base_url}/song?id={song_info.get("id", "")}',
                'play_count': song_info.get('playCount', 0),
            }
            
            song = self.save_song(song_data, artist, album)
            return song is not None
            
        except Exception as e:
            self.log('ERROR', f'解析歌曲信息失败: {str(e)}')
            return False