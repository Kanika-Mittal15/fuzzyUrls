from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .models import create_short_url

# URL validation regex
URL_REGEX = re.compile(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$")

@csrf_exempt
def shorten_url(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            original_url = data.get("url")

            # Validate URL
            if not original_url or not URL_REGEX.match(original_url):
                return JsonResponse({"error": "Invalid URL"}, status=400)

            # Generate short URL
            short_code = create_short_url(original_url)
            short_url = f"{request.get_host()}/{short_code}"

            return JsonResponse({"short_url": short_url}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)

db=settings.MONGO_DB

# Initialize MongoDB connection

def home(request):
    return JsonResponse({"message": "Welcome to FuzzyURLs Backend!"})

# Create your v
def test_mongo(request):
    db_status = "Connected" if db is not None else "Failed"
    return JsonResponse({"MongoDB Status": db_status})
