from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from home.models import Album, Artist, Review


class TestChartsView(TestCase):
    """
    Test cases for the charts view.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.artist = Artist.objects.create(
            artist_id="artist1", artist_name="Test Artist"
        )

        # Create multiple albums with varying ratings and review counts
        self.album1 = Album.objects.create(
            album_id="1",
            title="Album 1",
            artist=self.artist,
            artwork="http://www.artwork.com/1",
            released="2020-01-01",
        )
        self.album2 = Album.objects.create(
            album_id="2",
            title="Album 2",
            artist=self.artist,
            artwork="http://www.artwork.com/2",
            released="2020-01-02",
        )
        self.album3 = Album.objects.create(
            album_id="3",
            title="Album 3",
            artist=self.artist,
            artwork="http://www.artwork.com/3",
            released="2020-01-03",
        )
        self.album4 = Album.objects.create(
            album_id="4",
            title="Album 4",
            artist=self.artist,
            artwork="http://www.artwork.com/4",
            released="2020-01-04",
        )
        self.album5 = Album.objects.create(
            album_id="5",
            title="Album 5",
            artist=self.artist,
            artwork="http://www.artwork.com/5",
            released="2020-01-05",
        )
        self.album6 = Album.objects.create(
            album_id="6",
            title="Album 6",
            artist=self.artist,
            artwork="http://www.artwork.com/6",
            released="2020-01-06",
        )

        # Create reviews for the albums
        for album in [
            self.album1,
            self.album2,
            self.album3,
            self.album4,
            self.album5,
            self.album6,
        ]:
            Review.objects.create(
                album=album, author=self.user, rating=4, body="Good album"
            )
            Review.objects.create(
                album=album, author=self.user, rating=5, body="Excellent album"
            )

        # Update review counts and ratings to create distinctions
        Review.objects.create(
            album=self.album1, author=self.user, rating=3, body="Average album"
        )
        Review.objects.create(
            album=self.album2, author=self.user, rating=2, body="Not great"
        )
        Review.objects.create(
            album=self.album3, author=self.user, rating=1, body="Bad album"
        )
        Review.objects.create(
            album=self.album4, author=self.user, rating=5, body="Excellent album"
        )
        Review.objects.create(
            album=self.album5, author=self.user, rating=5, body="Excellent album"
        )
        Review.objects.create(
            album=self.album6, author=self.user, rating=5, body="Excellent album"
        )

    def test_charts_view_status_code(self):
        """Test that the charts view returns a 200 status code."""
        response = self.client.get(reverse("charts"))
        self.assertEqual(
            response.status_code,
            200,
            msg="Charts view did not return a 200 status code",
        )

    def test_charts_view_template_used(self):
        """Test that the charts view uses the correct template."""
        response = self.client.get(reverse("charts"))
        self.assertTemplateUsed(
            response,
            "charts/charts.html",
            msg_prefix="Charts view did not use the correct template",
        )

    def test_charts_view_context_top_album(self):
        """Test that the top album is correctly determined and passed to the context."""
        response = self.client.get(reverse("charts"))
        top_album = response.context["top_album"]
        self.assertIsNotNone(top_album, msg="Top album is not in the context")
        self.assertEqual(
            top_album.title, "Album 4", msg="Top album is not the expected album"
        )

    def test_charts_view_context_top_albums(self):
        """Test that the top albums (excluding the top album) are correctly determined and passed to the context."""
        response = self.client.get(reverse("charts"))
        top_albums = response.context["top_albums"]
        self.assertEqual(
            len(top_albums), 5, msg="Top albums list does not contain 5 albums"
        )
        self.assertNotIn(
            self.album4,
            top_albums,
            msg="Top album should not be in the top albums list",
        )

    def test_charts_view_context_most_reviewed_albums(self):
        """Test that the most reviewed albums are correctly determined and passed to the context."""
        response = self.client.get(reverse("charts"))
        most_reviewed_albums = response.context["most_reviewed_albums"]
        self.assertEqual(
            len(most_reviewed_albums),
            5,
            msg="Most reviewed albums list does not contain 5 albums",
        )
        self.assertEqual(
            most_reviewed_albums[0].title,
            "Album 1",
            msg="Most reviewed album is not the expected album",
        )
