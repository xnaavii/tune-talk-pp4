from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Artist(models.Model):
    artist_id = models.CharField(primary_key=True, max_length=50)
    artist_name = models.CharField(max_length=200)

    def __str__(self):
        return self.artist_name

class Album(models.Model):
    album_id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    artwork = models.URLField(blank=True, default='')
    released = models.CharField(max_length=200)

    class Meta:
        ordering = ["title"]

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        else:
            return 0

    def __str__(self):
        return self.title

class Review(models.Model):
    album= models.ForeignKey(Album, related_name="reviews", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.title} by {self.author} | {self.created_at}"
