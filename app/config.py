import os

class Config:
    """Database configuration for Poll Service"""
    DB_HOST = os.getenv("POLL_DB_HOST", "localhost")
    DB_PORT = int(os.getenv("POLL_DB_PORT", 3308))
    DB_USER = os.getenv("POLL_DB_USER", "root")
    DB_PASSWORD = os.getenv("POLL_DB_PASSWORD", "root_password")
    DB_NAME = os.getenv("POLL_DB_NAME", "poll_db")

    # User service URL for inter-service communication
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8001")

config = Config()
