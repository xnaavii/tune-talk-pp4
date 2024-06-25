from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
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
    
class Review(models.Model):
    album= models.ForeignKey(Album, related_name="reviews", on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
