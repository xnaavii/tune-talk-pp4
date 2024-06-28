from django.test import SimpleTestCase
from django.urls import reverse, resolve
from about.views import about_page

class TestAboutUrls(SimpleTestCase):
    """
    Test URL routing for the about app.

    This class defines test cases to verify that each URL in the about app correctly
    resolves to its corresponding view function.
    """
    def test_about_page_url_is_resolved(self):
        url = reverse('about_page')
        self.assertEqual(resolve(url).func, about_page)