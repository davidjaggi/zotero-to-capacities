# config.py
import os
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API tokens from environment variables
ZOTERO_USER_ID = os.getenv('ZOTERO_USER_ID')
ZOTERO_API_KEY = os.getenv('ZOTERO_API_KEY')
CAPACITIES_TOKEN = os.getenv('CAPACITIES_TOKEN')
CAPACITIES_SPACE_ID = os.getenv('CAPACITIES_SPACE_ID')

CAPACITIES_BASE_URL = 'https://api.capacities.io'

# Processing configuration
ITEMS_PER_RUN = 5
ITEMS_UPDATED_AFTER = "2024-11-01"

# File paths
PROCESSED_KEYS_FILE = Path('processed_keys.txt')

# Ensure the processed keys file exists
if not PROCESSED_KEYS_FILE.exists():
    PROCESSED_KEYS_FILE.touch()


def get_processed_keys():
    """Read the set of previously processed article IDs."""
    with open(PROCESSED_KEYS_FILE, 'r') as f:
        return set(line.strip() for line in f if line.strip())


def add_processed_key(article_id):
    """Add a newly processed article ID to the tracking file."""
    with open(PROCESSED_KEYS_FILE, 'a') as f:
        f.write(f'{article_id}\n')


def get_reference_timestamp() -> str:
    """
    Converts our reference date into the ISO 8601 format required by the Readwise API.
    Returns a properly formatted timestamp that includes time and timezone information.
    """
    try:
        reference_date = datetime.strptime(ITEMS_UPDATED_AFTER, "%Y-%m-%d")
        reference_timestamp = reference_date.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=timezone.utc
        )
        return reference_timestamp.isoformat()
    except ValueError as e:
        raise ValueError(f"Invalid reference date format in config: {e}")
