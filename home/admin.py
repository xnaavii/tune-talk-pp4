from django.contrib import admin
from .models import Artist, Album, Song, Review
# Register your models here.
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Review)