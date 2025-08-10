from django.contrib import admin
from .models import Song, Artist, Album, Platform


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'created_at']
    list_filter = ['platform', 'created_at']
    search_fields = ['name']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'platform', 'release_date', 'created_at']
    list_filter = ['platform', 'release_date', 'created_at']
    search_fields = ['title', 'artist__name']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'album', 'platform', 'duration', 'created_at']
    list_filter = ['platform', 'created_at']
    search_fields = ['title', 'artist__name', 'album__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_url', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']