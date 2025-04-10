import os
from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
