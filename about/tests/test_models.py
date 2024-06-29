from django.test import TestCase
from about.models import About


class TestAboutModel(TestCase):
    """
    Test the About model.

    This class defines test cases to verify that the About model is correctly
    saving and retrieving data.
    """

    def setUp(self):
        """Set up the test environment by creating an About instance."""
        self.about = About.objects.create(
            title="About Title", content="About Content")

    def test_about_model_creation(self):
        """Test that an About instance is created correctly."""
        self.assertEqual(
            self.about.title,
            "About Title",
            msg="The About instance title does not match the expected value",
        )
        self.assertEqual(
            self.about.content,
            "About Content",
            msg="The About instance content does not match the expected value",
        )

    def test_about_model_creation_incorrect(self):
        """Test that an About instance is not created correctly."""
        self.assertNotEqual(
            self.about.title,
            "About Titles",
            msg="The About instance title matches the expected value",
        )
        self.assertNotEqual(
            self.about.content,
            "About Contents",
            msg="The About instance content matches the expected value",
        )

    def test_about_model_str(self):
        """Test the string representation of the About instance."""
        self.assertEqual(
            str(self.about),
            "About Title",
            msg="The About instance string doesn't match the expected value"
        )

    def test_about_model_update(self):
        """Test updating an About instance."""
        self.about.title = "Updated Title"
        self.about.content = "Updated Content"
        self.about.save()
        updated_about = About.objects.get(id=self.about.id)
        self.assertEqual(
            updated_about.title,
            "Updated Title",
            msg="The About instance title was not updated correctly",
        )
        self.assertEqual(
            updated_about.content,
            "Updated Content",
            msg="The About instance content was not updated correctly",
        )
