from django.db import models
from django.utils import timezone


class Platform(models.Model):
    """音乐平台模型"""
    name = models.CharField(max_length=100, verbose_name='平台名称')
    base_url = models.URLField(verbose_name='平台基础URL')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '音乐平台'
        verbose_name_plural = '音乐平台'
        
    def __str__(self):
        return self.name


class Artist(models.Model):
    """艺术家模型"""
    name = models.CharField(max_length=200, verbose_name='艺术家名称')
    avatar = models.ImageField(upload_to='artists/', blank=True, null=True, verbose_name='头像')
    biography = models.TextField(blank=True, verbose_name='简介')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, verbose_name='来源平台')
    platform_id = models.CharField(max_length=100, verbose_name='平台ID')
    platform_url = models.URLField(blank=True, verbose_name='平台链接')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '艺术家'
        verbose_name_plural = '艺术家'
        unique_together = ['platform', 'platform_id']
        
    def __str__(self):
        return f"{self.name} ({self.platform.name})"


class Album(models.Model):
    """专辑模型"""
    title = models.CharField(max_length=200, verbose_name='专辑标题')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='艺术家')
    cover = models.ImageField(upload_to='albums/', blank=True, null=True, verbose_name='专辑封面')
    description = models.TextField(blank=True, verbose_name='专辑描述')
    release_date = models.DateField(blank=True, null=True, verbose_name='发行日期')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, verbose_name='来源平台')
    platform_id = models.CharField(max_length=100, verbose_name='平台ID')
    platform_url = models.URLField(blank=True, verbose_name='平台链接')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '专辑'
        verbose_name_plural = '专辑'
        unique_together = ['platform', 'platform_id']
        
    def __str__(self):
        return f"{self.title} - {self.artist.name}"


class Song(models.Model):
    """歌曲模型"""
    title = models.CharField(max_length=200, verbose_name='歌曲标题')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='艺术家')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True, verbose_name='专辑')
    duration = models.PositiveIntegerField(blank=True, null=True, verbose_name='时长(秒)')
    lyrics = models.TextField(blank=True, verbose_name='歌词')
    genre = models.CharField(max_length=100, blank=True, verbose_name='音乐类型')
    
    # 平台相关信息
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, verbose_name='来源平台')
    platform_id = models.CharField(max_length=100, verbose_name='平台ID')
    platform_url = models.URLField(blank=True, verbose_name='平台链接')
    
    # 音频文件信息
    audio_url = models.URLField(blank=True, verbose_name='音频链接')
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True, verbose_name='音频文件')
    
    # 统计信息
    play_count = models.PositiveIntegerField(default=0, verbose_name='播放次数')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '歌曲'
        verbose_name_plural = '歌曲'
        unique_together = ['platform', 'platform_id']
        
    def __str__(self):
        return f"{self.title} - {self.artist.name}"
    
    def duration_display(self):
        """格式化显示时长"""
        if self.duration:
            minutes = self.duration // 60
            seconds = self.duration % 60
            return f"{minutes:02d}:{seconds:02d}"
        return "未知"