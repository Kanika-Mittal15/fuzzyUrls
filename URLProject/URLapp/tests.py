from django.test import TestCase
from django.urls import reverse
import json

class URLShortenerTests(TestCase):

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