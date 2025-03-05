from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from pymongo import MongoClient

# Initialize MongoDB connection
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]


def home(request):
    return JsonResponse({"message": "Welcome to FuzzyURLs Backend!"})

# Create your v
def test_mongo(request):
    db_status = "Connected" if db is not None else "Failed"
    return JsonResponse({"MongoDB Status": db_status})
