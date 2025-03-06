from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from .models import url_collection

class URLShortenerTests(TestCase):

    def setUp(self):
        """
        Set up test data before each test case.
        """
        self.original_url = "https://example.com"
        self.short_code = "abc12345"

        # Insert a test URL into MongoDB
        url_collection.insert_one({
            "original_url": self.original_url,
            "short_code": self.short_code
        })

    def test_redirection_success(self):
        """
        Test that a valid short code redirects to the correct original URL.
        """
        response = self.client.get(reverse("redirect_to_original", args=[self.short_code]))
        self.assertEqual(response.status_code, 302)  # 302 is HTTP redirect
        self.assertEqual(response.url, self.original_url)

    def test_redirection_not_found(self):
        """
        Test that an invalid short code returns a 404 error.
        """
        response = self.client.get(reverse("redirect_to_original", args=["invalid123"]))
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {"error": "Short URL not found"})