import uuid
from django.conf import settings

# Get the MongoDB connection
db=settings.MONGO_DB

# Collection reference
if not hasattr(db, "list_collection_names"):
    raise TypeError("MONGO_DB is not a valid MongoDB database instance")

url_collection = db["urls"]

def create_short_url(original_url):
    """Generates a short URL and stores it in MongoDB"""
    # Generate a unique short code
    short_code = str(uuid.uuid4())[:8]

    # Store in MongoDB
    url_collection.insert_one({
        "original_url": original_url,
        "short_code": short_code
    })

    return short_code

# Create your models here.
