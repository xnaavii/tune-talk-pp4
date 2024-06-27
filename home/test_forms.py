from django.test import TestCase
from .forms import ReviewForm


class TestReviewForm(TestCase):

    def test_form_is_valid(self):
        review_form = ReviewForm({'title': 'This is great', 'body': 'This is a great album', 'rating': 1})
        self.assertTrue(review_form.is_valid(), msg="Form is not valid")
    
    def test_form_is_invalid(self):
        review_form = ReviewForm({'title': 'This is great', 'body': 'This is a great album', 'rating': 0})
        self.assertFalse(review_form.is_valid(), msg="Form is valid")