from rest_framework import serializers
from .models import Song, Artist, Album, Platform


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    
    class Meta:
        model = Artist
        fields = ['id', 'name', 'avatar', 'biography', 'platform', 
                 'platform_name', 'platform_id', 'platform_url', 
                 'created_at', 'updated_at']


class AlbumSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.name', read_only=True)
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    
    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'artist_name', 'cover', 
                 'description', 'release_date', 'platform', 
                 'platform_name', 'platform_id', 'platform_url',
                 'created_at', 'updated_at']


class SongSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.name', read_only=True)
    album_title = serializers.CharField(source='album.title', read_only=True)
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    duration_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'artist_name', 'album', 
                 'album_title', 'duration', 'duration_display', 'lyrics', 
                 'genre', 'platform', 'platform_name', 'platform_id', 
                 'platform_url', 'audio_url', 'audio_file', 'play_count', 
                 'like_count', 'created_at', 'updated_at']