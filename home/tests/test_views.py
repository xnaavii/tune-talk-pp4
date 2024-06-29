from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from unittest.mock import patch
from home.models import Album, Review, Artist


class TestHomeViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        self.artist = Artist.objects.create(
            artist_id="artistid", artist_name="Test Artist"
        )

        self.album = Album.objects.create(
            album_id="6vuykQgDLUCiZ7YggIpLM9",
            # Make sure this title matches your expected test case
            title="Test Album",
            artist=self.artist,
            artwork="http://www.artwork.com",
            released=datetime(2000, 1, 29),
        )

        self.review = Review.objects.create(
            album=self.album,
            author=self.user,
            title="Review Title",
            rating=3,
            body="Review Body",
            created_at=datetime(2024, 6, 28, 12, 0, 0),
        )

        self.client = Client()
        self.client.login(username="testuser", password="password123")

        # URLs for testing
        self.album_list_url = reverse("album_list")
        self.album_detail_url = reverse(
            "album_detail", args=[self.album.album_id]
            )
        self.edit_review_url = reverse(
            "edit_review", args=[self.album.album_id, 1]
        )  # Review ID will be set in the test
        self.delete_review_url = reverse(
            "delete_review", args=[self.album.album_id, 1]
        )  # Review ID will be set in the test
        self.home_url = reverse("home")

    def test_album_list_view_GET(self):
        """Test album_list view for rendering and context."""
        response = self.client.get(reverse("album_list"))
        self.assertEqual(
            response.status_code,
            200,
            msg="album_list view did not return 200 status code",
        )
        self.assertTemplateUsed(response, "home/album_list.html")

    @patch(
        "home.spotify_utils.get_spotify_client"
    )  # Patch the function to mock Spotify client
    def test_album_detail_view_GET(self, mock_get_spotify_client):
        """
        Test album_detail view for rendering, context, and review creation.
        """
        # Mock Spotify API response
        mock_album_data = {
            "id": "test_album_id",
            # Adjust the expected name here
            "name": "Test Album",
            "artists": [{"name": "Test Artist"}],
            "release_date": "2024-01-01",
            "images": [{"url": "https://example.com/image.jpg"}],
        }

        # Configure mock return value for Spotify client
        mock_spotify_client = mock_get_spotify_client.return_value
        mock_spotify_client.album.return_value = mock_album_data

        # Make request to album_detail view
        response = self.client.get(self.album_detail_url)
        self.assertEqual(
            response.status_code,
            200,
            msg="album_detail view did not return 200 status code",
        )
        self.assertTemplateUsed(response, "home/album_detail.html")
        # Check context data
        self.assertIn("album", response.context)
        self.assertEqual(response.context["album"].title, "Test Album")

        # Test review creation
        review_data = {
            "title": "I like this",
            "rating": 5,
            "body": "This album is awesome!",
        }
        response_post = self.client.post(
            reverse("album_detail", args=[self.album.album_id]), review_data
        )
        self.assertEqual(
            response_post.status_code, 302
            )  # Should redirect after POST
        self.assertTrue(
            Review.objects.filter(body="This album is awesome!").exists()
            )

    @patch(
        "home.spotify_utils.get_spotify_client"
    )  # Patch the function to mock Spotify client
    def test_album_detail_view_POST(self, mock_get_spotify_client):
        """Test album_detail view for review creation."""
        # Mock Spotify API response
        mock_album_data = {
            "id": "test_album_id",
            "name": "Test Album",  # Adjust the expected name here
            "artists": [{"name": "Test Artist"}],
            "release_date": "2024-01-01",
            "images": [{"url": "https://example.com/image.jpg"}],
        }

        # Configure mock return value for Spotify client
        mock_spotify_client = mock_get_spotify_client.return_value
        mock_spotify_client.album.return_value = mock_album_data

        # Test review creation
        review_data = {
            "title": "I like this",
            "rating": 5,
            "body": "This album is awesome!",
        }
        response_post = self.client.post(self.album_detail_url, review_data)
        self.assertEqual(
            response_post.status_code, 302
            )  # Should redirect after POST
        self.assertTrue(
            Review.objects.filter(body="This album is awesome!").exists()
            )

    def test_edit_review_view_GET(self):
        """
        Test edit_review view for rendering.
        """
        # Create a review for the album
        review = self.review
        # Make request to edit_review view
        edit_url = reverse(
            "edit_review", args=[self.album.album_id, review.id]
            )
        response = self.client.get(edit_url)
        self.assertEqual(
            response.status_code,
            200,
            msg="Edit review view did not return 200 status code",
        )
        self.assertTemplateUsed(response, "home/edit_review.html")
        # Check initial form values
        self.assertContains(response, "Review Title")
        self.assertContains(response, "Review Body")

    def test_edit_review_view_POST(self):
        """
        Test edit_review view for editing a review.
        """
        # Create a review for the album
        review = self.review

        edit_url = reverse(
            "edit_review", args=[self.album.album_id, review.id]
            )
        # Update review data
        updated_review_data = {
            "title": "Updated Review",
            "rating": 5,
            "body": "Updated review body",
        }
        response_post = self.client.post(edit_url, updated_review_data)
        # Should redirect after POST
        self.assertEqual(
            response_post.status_code,
            302,
            msg="Edit review view did not redirect after POST",
        )
        self.assertTrue(
            Review.objects.filter(body="Updated review body").exists()
            )

    def test_delete_review_view_POST(self):

        # Create a review for the album
        review = self.review

        # Make request to delete_review view
        delete_url = reverse(
            "delete_review", args=[self.album.album_id, review.id]
            )
        response = self.client.post(delete_url)
        self.assertEqual(
            response.status_code,
            302,
            msg="Delete review view did not redirect after POST",
        )
        self.assertFalse(
            Review.objects.filter(id=review.id).exists(),
            msg="Review was not deleted successfully",
        )

    def test_home_view(self):
        """Test home view for rendering and context."""
        response = self.client.get(reverse("home"))
        self.assertEqual(
            response.status_code, 200,
            msg="Home view did not return 200 status code"
        )
        self.assertTemplateUsed(response, "home/homepage.html")

        # Check if albums and latest_reviews are in the context
        self.assertIn(
            "albums", response.context,
            msg="Context missing 'albums'")
        self.assertIn(
            "latest_reviews", response.context,
            msg="Context missing 'latest_reviews'"
        )

        # Check if there are no albums with average rating > 5
        self.assertFalse(
            Album.objects.filter(reviews__rating__gt=5).exists(),
            msg="Albums with rating > 5 found in context",
        )

        # Ensure albums are ordered correctly by average_rating and num_reviews
        if "albums" in response.context:
            albums = response.context["albums"]
            if albums:
                for i in range(len(albums) - 1):
                    self.assertGreaterEqual(
                        albums[i].average_rating,
                        albums[i + 1].average_rating,
                        msg="Albums not ordered correctly by average rating",
                    )
                    self.assertGreaterEqual(
                        albums[i].num_reviews,
                        albums[i + 1].num_reviews,
                        msg="Albums not ordered correctly by num of reviews",
                    )
