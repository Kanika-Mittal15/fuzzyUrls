from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
import json
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

    def test_shorten_valid_url(self):
        """
        Test that a valid URL is successfully shortened.
        """
        response = self.client.post(
            reverse("shorten_url"),
            data=json.dumps({"url": "https://example.com"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("short_url", response.json())

    def test_shorten_invalid_url(self):
        """
        Test that an invalid URL returns a 400 Bad Request.
        """
        response = self.client.post(
            reverse("shorten_url"),
            data=json.dumps({"url": "invalid-url"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Invalid URL"})

    def test_shorten_invalid_json(self):
        """
        Test that a request with invalid JSON returns a 400 Bad Request.
        """
        response = self.client.post(
            reverse("shorten_url"),
            data="Invalid JSON Data",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Invalid JSON"})

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