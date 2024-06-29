from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home.views import (album_list,
                        album_detail,
                        edit_review,
                        delete_review,
                        home)


class TestHomeUrls(SimpleTestCase):
    """
    Test URL routing for the home app.

    This class test cases ensure that each URL in the home app correctly
    resolves to its view function. It includes positive tests to ensure
    correct resolutions and negative tests to check that URLs do not resolve to
    incorrect views.
    """

    def test_album_list_url_is_resolved(self):
        url = reverse("album_list")
        self.assertEqual(
            resolve(url).func,
            album_list,
            msg="The album_list URL did not resolve to album_list view",
        )

    def test_album_list_url_is__not_resolved_to_home(self):
        url = reverse("album_list")
        self.assertNotEqual(
            resolve(url).func,
            home,
            msg="The album_list URL incorrectly resolved to home view",
        )

    def test_album_detail_url_is_resolved(self):
        album_id = "album_id"
        url = reverse("album_detail", args=[album_id])
        self.assertEqual(
            resolve(url).func,
            album_detail,
            msg="The album_detail URL did not resolve to album_detail view",
        )

    def test_album_detail_url_is_not_resolved_to_album_list(self):
        album_id = "album_id"
        url = reverse("album_detail", args=[album_id])
        self.assertNotEqual(
            resolve(url).func,
            album_list,
            msg="The album_detail URL incorrectly resolved to album_list view",
        )

    def test_edit_review_url_is_resolved(self):
        album_id = "6vuykQgDLUCiZ7YggIpLM9"
        review_id = 1
        url = reverse("edit_review", args=[album_id, review_id])
        self.assertEqual(
            resolve(url).func,
            edit_review,
            msg="The URL did not resolve to edit_review view",
        )

    def test_edit_review_url_is_not_resolved_to_album_detail(self):
        album_id = "6vuykQgDLUCiZ7YggIpLM9"
        review_id = 1
        url = reverse("edit_review", args=[album_id, review_id])
        self.assertNotEqual(
            resolve(url).func,
            album_detail,
            msg="The URL incorrectly resolved to album_detail view",
        )

    def test_delete_review_url_is_resolved(self):
        album_id = "6vuykQgDLUCiZ7YggIpLM9"
        review_id = 1
        url = reverse("delete_review", args=[album_id, review_id])
        self.assertEqual(
            resolve(url).func,
            delete_review,
            msg="The delete_review URL did not resolve to delete_review view",
        )

    def test_delete_review_url_is_not_resolved_to_edit_review(self):
        album_id = "6vuykQgDLUCiZ7YggIpLM9"
        review_id = 1
        url = reverse("delete_review", args=[album_id, review_id])
        self.assertNotEqual(
            resolve(url).func,
            edit_review,
            msg="The URL incorrectly resolved to edit_review view",
        )

    def test_home_url_is_resolved(self):
        url = reverse("home")
        self.assertEqual(
            resolve(url).func, home,
            msg="The home URL did not resolve to home view"
        )

    def test_home_url_is_not_resolved_to_album_list(self):
        url = reverse("home")
        self.assertNotEqual(
            resolve(url).func,
            album_list,
            msg="The URL incorrectly resolved to album_list view",
        )
