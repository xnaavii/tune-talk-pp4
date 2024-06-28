from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from home.models import Review, Album, Artist
from datetime import datetime


class TestReviewsView(TestCase):
    """
    Test cases for the reviews view.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.artist = Artist.objects.create(
            artist_id="artist1", artist_name="Test Artist"
        )
        self.album = Album.objects.create(
            album_id="album1",
            title="Test Album",
            artist=self.artist,
            released=datetime(2020, 1, 1),
            artwork="http://www.artwork.com/1",
        )

        # Create multiple reviews
        self.review1 = Review.objects.create(
            album=self.album,
            author=self.user,
            title="Review 1",
            body="This is review body 1",
            rating=1,
            created_at=datetime(2024, 6, 28, 12, 0, 0),
        )

        self.review2 = Review.objects.create(
            album=self.album,
            author=self.user,
            title="Review 2",
            body="This is review body 2",
            rating=2,
            created_at=datetime(2024, 6, 29, 12, 0, 0),
        )

        self.review3 = Review.objects.create(
            album=self.album,
            author=self.user,
            title="Review 3",
            body="This is review body 3",
            rating=3,
            created_at=datetime(2024, 6, 30, 12, 0, 0),
        )

        self.review4 = Review.objects.create(
            album=self.album,
            author=self.user,
            title="Review 4",
            body="This is review body 4",
            rating=4,
            created_at=datetime(2024, 7, 1, 12, 0, 0),
        )

        self.review5 = Review.objects.create(
            album=self.album,
            author=self.user,
            title="Review 5",
            body="This is review body 5",
            rating=5,
            created_at=datetime(2024, 7, 2, 12, 0, 0),
        )

        self.reviews_url = reverse("reviews")

    def test_reviews_view_status_code(self):
        """Test that the reviews view returns a 200 status code."""
        response = self.client.get(self.reviews_url)
        self.assertEqual(
            response.status_code,
            200,
            msg="Reviews view did not return a 200 status code",
        )

    def test_reviews_view_search_title(self):
        """Test the search functionality by title."""
        response = self.client.get(self.reviews_url, {"search": "Review 1"})
        self.assertEqual(
            response.context["all_reviews"].count(),
            1,
            msg="Search by title did not return the correct number of reviews",
        )
        self.assertEqual(
            response.context["all_reviews"].first().title,
            "Review 1",
            msg="Search by title did not return the correct review",
        )

    def test_reviews_view_search_body(self):
        """Test the search functionality by body."""
        response = self.client.get(self.reviews_url, {"search": "review body 2"})
        self.assertEqual(
            response.context["all_reviews"].count(),
            1,
            msg="Search by body did not return the correct number of reviews",
        )
        self.assertEqual(
            response.context["all_reviews"].first().body,
            "This is review body 2",
            msg="Search by body did not return the correct review",
        )
