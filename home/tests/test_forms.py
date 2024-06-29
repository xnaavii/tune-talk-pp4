from django.test import TestCase
from home.forms import ReviewForm


class TestReviewForm(TestCase):
    """
    Test cases for ReviewForm.
    """

    def test_form_is_valid(self):
        """Test form with valid data."""
        review_form = ReviewForm(
            {"title": "This is great",
                "body": "This is a great album",
                "rating": 1}
            )
        self.assertTrue(review_form.is_valid(), msg="Form should be valid")

    def test_form_is_invalid(self):
        """Test form with invalid rating."""
        review_form = ReviewForm(
            {"title": "This is great",
                "body": "This is a great album",
                "rating": 0}
            )
        self.assertFalse(
            review_form.is_valid(),
            msg="Form should be invalid due to invalid rating"
        )

    def test_form_missing_title(self):
        """Test form missing title."""
        review_form = ReviewForm(
            {"title": "",
                "body": "This is a great album",
                "rating": 3}
            )
        self.assertFalse(
            review_form.is_valid(),
            msg="Form should be invalid due to missing title"
        )
        self.assertIn("title", review_form.errors)

    def test_form_missing_body(self):
        """Test form missing body."""
        review_form = ReviewForm(
            {"title": "This is great",
                "body": "",
                "rating": 3}
            )
        self.assertFalse(
            review_form.is_valid(),
            msg="Form should be invalid due to missing body"
        )
        self.assertIn("body", review_form.errors)
