from django.test import TestCase
from django.urls import reverse
from about.models import About


class TestAboutPageViews(TestCase):
    """
    Test the about page views.

    This class defines test cases to verify that,
    the about page renders correctly,
    uses the correct template, and contains the expected content.
    """

    def setUp(self):
        """Set up the test environment by creating an About instance."""
        self.about = About.objects.create(title="title", content="content")

    def test_about_page_view(self):
        """Test that the about page
        view renders correctly and uses the correct template.
        """
        response = self.client.get(
            reverse("about_page"))
        self.assertEqual(
            response.status_code,
            200,
            msg="The about page did not return a 200 status code",
        )
        self.assertTemplateUsed(
            response,
            "about/about.html",
            msg_prefix="The about page did not use the correct template",
        )

    def test_about_page_contains_title(self):
        """Test that the about page
        contains the correct title in its context.
        """
        response = self.client.get(reverse("about_page"))
        self.assertContains(
            response,
            "title",
            msg_prefix="The about page did not contain the expected title",
        )

    def test_about_page_contains_no_title(self):
        """Test that the about page contains
        the incorrect title in its context.
        """
        response = self.client.get(reverse("about_page"))
        self.assertNotContains(
            response,
            "incorrect title",
            msg_prefix="The about page contains the expected title",
        )

    def test_about_page_contains_content(self):
        """
        Test that the about page contains the correct content in its context.
        """
        response = self.client.get(reverse("about_page"))
        self.assertContains(
            response,
            "content",
            msg_prefix="The about page did not contain the expected content",
        )

    def test_about_page_contains_no_content(self):
        """
        Test that the about page contains the incorrect content in its context.
        """
        response = self.client.get(reverse("about_page"))
        self.assertNotContains(
            response,
            "incorrect content",
            msg_prefix="The about page contains the expected content",
        )
