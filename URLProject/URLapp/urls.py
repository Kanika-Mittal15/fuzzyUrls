from django.urls import path
from .views import home,test_mongo,shorten_url


urlpatterns = [
    path('', home, name='home'),
    path('test_mongo/', test_mongo, name='test_mongo'),
    path("shorten/", shorten_url, name="shorten_url"),
]