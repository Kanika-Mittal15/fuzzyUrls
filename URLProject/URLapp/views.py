from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .models import create_short_url,url_collection # Import MongoDB collection


# Initialize MongoDB connection
db=settings.MONGO_DB 

def redirect_to_original(request, short_code):
    """
    Redirects the user to the original URL if the short code exists in MongoDB.
    """
    # Query MongoDB for the short_code
    result = url_collection.find_one({"short_code": short_code})

    if result:
        original_url = result["original_url"]
        return HttpResponseRedirect(original_url)  # Redirect to the original URL
    else:
        return JsonResponse({"error": "Short URL not found"}, status=404)

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


def home(request):
    return JsonResponse({"message": "Welcome to FuzzyURLs Backend!"})

# Create your v
def test_mongo(request):
    db_status = "Connected" if db is not None else "Failed"
    return JsonResponse({"MongoDB Status": db_status})
