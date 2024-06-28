from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reviews.views import reviews


class TestChartsUrls(SimpleTestCase):
    """
    Test URL routing for the reviews app.

    This class defines test cases to verify that each URL in the reviews app correctly
    resolves to its corresponding view function.
    """

    def test_charts_page_url_is_resolved(self):
        url = reverse("reviews")
        self.assertEqual(resolve(url).func, reviews)
