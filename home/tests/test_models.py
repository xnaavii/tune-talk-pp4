from django.test import TestCase
from datetime import datetime
from home.models import Album, Artist, Review
from django.contrib.auth.models import User


class TestModels(TestCase):
    """
    Test cases for Album, Artist, and Review models.
    """

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.artist = Artist.objects.create(
            artist_id="artistid", artist_name="Test Artist"
        )
        self.album = Album.objects.create(
            album_id="6vuykQgDLUCiZ7YggIpLM9",
            title="Test Album",
            artist=self.artist,
            artwork="http://www.artwork.com",
            released="29-01-2000",
        )
        self.review = Review.objects.create(
            album=self.album,
            author=self.user,
            title="Test Review",
            rating=4,
            body="Test review body",
            created_at=datetime.now(),
        )

    def test_album_model(self):
        """Test Album model."""
        album = Album.objects.get(album_id="6vuykQgDLUCiZ7YggIpLM9")
        self.assertEqual(album.title, "Test Album")
        self.assertEqual(album.artist, self.artist)
        self.assertEqual(album.artwork, "http://www.artwork.com")
        self.assertEqual(album.released, "29-01-2000")

    def test_artist_model(self):
        """Test Artist model."""
        artist = Artist.objects.get(artist_id="artistid")
        self.assertEqual(artist.artist_name, "Test Artist")

    def test_review_model(self):
        """Test Review model."""
        review = Review.objects.get(title="Test Review")
        self.assertEqual(review.album, self.album)
        self.assertEqual(review.author, self.user)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.body, "Test review body")
        self.assertIsInstance(review.created_at, datetime)

    def tearDown(self):
        """Clean up after each test."""
        self.user.delete()
        self.artist.delete()
        self.album.delete()
        self.review.delete()
