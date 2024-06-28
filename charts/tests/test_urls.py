from django.test import SimpleTestCase
from django.urls import reverse, resolve
from charts.views import charts


class TestChartsUrls(SimpleTestCase):
    """
    Test URL routing for the about app.

    This class defines test cases to verify that each URL in the charts app correctly
    resolves to its corresponding view function.
    """

    def test_charts_page_url_is_resolved(self):
        url = reverse("charts")
        self.assertEqual(resolve(url).func, charts)
