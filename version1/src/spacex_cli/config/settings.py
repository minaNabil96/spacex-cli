import os
from dotenv import load_dotenv

load_dotenv()


def get_api_url() -> str:
    return os.getenv("SPACEX_API_URL", "https://lldev.thespacedevs.com/2.2.0").rstrip("/")


def get_timeout() -> int:
    return int(os.getenv("REQUEST_TIMEOUT", "30"))
