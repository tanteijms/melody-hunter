from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.CrawlTaskViewSet)
router.register(r'logs', views.CrawlLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]