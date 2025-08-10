from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Song, Artist, Album, Platform
from .serializers import SongSerializer, ArtistSerializer, AlbumSerializer, PlatformSerializer


class PlatformViewSet(viewsets.ModelViewSet):
    """音乐平台视图集"""
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']


class ArtistViewSet(viewsets.ModelViewSet):
    """艺术家视图集"""
    queryset = Artist.objects.select_related('platform').all()
    serializer_class = ArtistSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']


class AlbumViewSet(viewsets.ModelViewSet):
    """专辑视图集"""
    queryset = Album.objects.select_related('artist', 'platform').all()
    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform', 'artist']
    search_fields = ['title', 'artist__name']
    ordering_fields = ['title', 'release_date', 'created_at']
    ordering = ['-created_at']


class SongViewSet(viewsets.ModelViewSet):
    """歌曲视图集"""
    queryset = Song.objects.select_related('artist', 'album', 'platform').all()
    serializer_class = SongSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform', 'artist', 'album', 'genre']
    search_fields = ['title', 'artist__name', 'album__title', 'lyrics']
    ordering_fields = ['title', 'duration', 'play_count', 'like_count', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """获取热门歌曲"""
        popular_songs = self.queryset.order_by('-play_count')[:20]
        serializer = self.get_serializer(popular_songs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def play(self, request, pk=None):
        """播放歌曲（增加播放次数）"""
        song = self.get_object()
        song.play_count += 1
        song.save()
        return Response({'message': '播放次数已更新', 'play_count': song.play_count})