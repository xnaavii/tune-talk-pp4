from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Artist(models.Model):
    artist_id = models.CharField(primary_key=True, max_length=50)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Album(models.Model):
    album_id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    artwork = models.URLField(blank=True, default='')
    songlist = models.TextField()
    released = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Song(models.Model):
    song_id = models.CharField(primary_key=True, max_length=50)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name="songs" ,on_delete=models.RESTRICT)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title