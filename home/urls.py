from . import views
from django.urls import path

urlpatterns = [
    path('', views.album_list, name="album_list"),
]
