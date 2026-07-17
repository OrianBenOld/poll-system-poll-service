import os
from databases import Database
from ..config import config

# Support both direct DATABASE_URL env var and individual config vars
if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.getenv("DATABASE_URL")
else:
    DATABASE_URL = f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

database = Database(DATABASE_URL)
