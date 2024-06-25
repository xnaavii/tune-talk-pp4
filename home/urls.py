from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('albums', views.album_list, name="album_list")
]
