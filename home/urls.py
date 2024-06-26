from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.album_list, name="album_list"),
    path('search/<str:album_id>', views.album_detail, name="album_detail")
]
