from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.album_list, name="album_list")
]
