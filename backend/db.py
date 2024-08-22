from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def init_db(app):
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
    return client[os.getenv("DB_NAME")] 
