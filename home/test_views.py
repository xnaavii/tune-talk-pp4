from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from unittest.mock import patch
from .models import Album, Review, Artist

class TestHomeViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123'
        )

        self.artist = Artist.objects.create(
            artist_id="artistid",
            artist_name="Test Artist"
        )

        self.album = Album.objects.create(
            album_id="6vuykQgDLUCiZ7YggIpLM9",
            title="Test Album",  # Make sure this title matches your expected test case
            artist=self.artist,
            artwork="http://www.artwork.com",
            released=datetime(2000, 1, 29)
        )

        self.client = Client()
        self.client.login(username='testuser', password='password123')


    def test_album_list_view(self):
        """Test album_list view for rendering and context."""
        response = self.client.get(reverse('album_list'))
        self.assertEqual(response.status_code, 200, msg="album_list view did not return 200 status code")
        self.assertTemplateUsed(response, 'home/album_list.html')
    
    @patch('home.spotify_utils.get_spotify_client')  # Patch the function to mock Spotify client
    def test_album_detail_view(self, mock_get_spotify_client):
        """
        Test album_detail view for rendering, context, and review creation.
        """
        # Mock Spotify API response
        mock_album_data = {
            'id': 'test_album_id',
            'name': 'Test Album',  # Adjust the expected name here
            'artists': [{'name': 'Test Artist'}],
            'release_date': '2024-01-01',
            'images': [{'url': 'https://example.com/image.jpg'}]
        }

        # Configure mock return value for Spotify client
        mock_spotify_client = mock_get_spotify_client.return_value
        mock_spotify_client.album.return_value = mock_album_data

        # Make request to album_detail view
        response = self.client.get(reverse('album_detail', args=[self.album.album_id]))
        self.assertEqual(response.status_code, 200, msg="album_detail view did not return 200 status code")
        self.assertTemplateUsed(response, 'home/album_detail.html')

        # Check context data
        self.assertIn('album', response.context)
        self.assertEqual(response.context['album'].title, 'Test Album')

        # Test review creation
        review_data = {
            'title': 'I like this',
            'rating': 5,
            'body': 'This album is awesome!'
        }
        response_post = self.client.post(reverse('album_detail', args=[self.album.album_id]), review_data)
        self.assertEqual(response_post.status_code, 302)  # Should redirect after POST
        self.assertTrue(Review.objects.filter(body='This album is awesome!').exists())

        
    def test_edit_review_view(self):
        """
        Test edit_review view for rendering and editing a review.
        """
        # Create a review for the album
        review = Review.objects.create(
            album=self.album,
            author=self.user,
            title="Initial Review",
            rating=4,
            body="Initial review body",
            created_at=datetime(2024, 6, 28, 12, 0, 0)
        )

        # Log in client
        self.client.login(username='testuser', password='password123')

        # Make request to edit_review view
        edit_url = reverse('edit_review', args=[self.album.album_id, review.id])
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200, "Edit review view did not return 200 status code")
        self.assertTemplateUsed(response, 'home/edit_review.html')

        # Check initial form values
        self.assertContains(response, "Initial Review")
        self.assertContains(response, "Initial review body")

        # Update review data
        updated_review_data = {
            'title': 'Updated Review',
            'rating': 5,
            'body': 'Updated review body'
        }
        response_post = self.client.post(edit_url, updated_review_data)
        # Should redirect after POST
        self.assertEqual(response_post.status_code, 302, msg="Edit review view did not redirect after POST") 
        self.assertTrue(Review.objects.filter(body='Updated review body').exists())

    def test_delete_review_view(self):
        """
        Test delete_review view for deleting a review.
        """
        # Create a review for the album
        review = Review.objects.create(
            album=self.album,
            author=self.user,
            title="Review to Delete",
            rating=3,
            body="Review body to delete",
            created_at=datetime(2024, 6, 28, 12, 0, 0)
        )

        # Log in client
        self.client.login(username='testuser', password='password123')

        # Make request to delete_review view
        delete_url = reverse('delete_review', args=[self.album.album_id, review.id])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302, msg="Delete review view did not redirect after POST")
        self.assertFalse(Review.objects.filter(id=review.id).exists(), msg="Review was not deleted successfully")

    def test_home_view(self):
        """Test home view for rendering and context."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200, msg="Home view did not return 200 status code")
        self.assertTemplateUsed(response, 'home/homepage.html')

        # Check if albums and latest_reviews are in the context
        self.assertIn('albums', response.context, msg="Context missing 'albums'")
        self.assertIn('latest_reviews', response.context, msg="Context missing 'latest_reviews'")

        # Check if there are no albums with average rating > 5
        self.assertFalse(Album.objects.filter(reviews__rating__gt=5).exists(), msg="Albums with rating > 5 found in context")