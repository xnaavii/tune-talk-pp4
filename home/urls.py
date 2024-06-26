from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.album_list, name="album_list"),
    path('albums/<str:album_id>', views.album_detail, name="album_detail"),
    path('albums/<str:album_id>/edit_review/<int:review_id>/', views.edit_review, name="edit_review"),
    path('albums/<str:album_id>/delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]
