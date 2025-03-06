from django.urls import path
from .views import home,test_mongo,shorten_url, redirect_to_original

urlpatterns = [
    path('', home, name='home'),
    path('test_mongo/', test_mongo, name='test_mongo'),
    path("shorten/", shorten_url, name="shorten_url"),
    path("<str:short_code>/", redirect_to_original, name="redirect_to_original"),  # New redirection route
]