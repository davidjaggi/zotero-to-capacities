import requests
import logging
from datetime import datetime, timezone
from time import sleep
from typing import Optional, Dict, List
from capacities_client import CapacitiesClient
from pathlib import Path
from pyzotero import zotero

from config import (
    ZOTERO_USER_ID,
    ZOTERO_API_KEY,
    CAPACITIES_TOKEN,
    CAPACITIES_SPACE_ID,
    ITEMS_PER_RUN,
    ITEMS_UPDATED_AFTER,
    get_processed_keys,
    add_processed_key,
    get_reference_timestamp
)

# Set up logging to help us track what's happening when the script runs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    capacities_client = CapacitiesClient(CAPACITIES_TOKEN, CAPACITIES_SPACE_ID)
    zotero_client = zotero.Zotero(ZOTERO_USER_ID, 'user', ZOTERO_API_KEY)

    processed_keys = get_processed_keys()


    reference_timestamp = get_reference_timestamp()
    logger.info(f"Fetching Zotero items updated after {ITEMS_UPDATED_AFTER}...")
    all_unprocessed_items = zotero_client.top(limit=5)
    logger.info(f"Found {len(all_unprocessed_items)} total items in Zotero library.")
    process_count = 0
    for item in all_unprocessed_items[:1]:
        item_key = item['data']['key']
        if item_key in processed_keys:
            logger.info(f"Skipping already processed item: {item['data']['title']}")
            continue
        """
        item_timestamp = item['meta']['updated']
        if item_timestamp < reference_timestamp:
            logger.info(f"Skipping item not updated after reference date: {item['data']['title']}")
            continue
        """

        logger.info(f"Processing item: {item['data']['title']}")
        capacities_client.create_weblink(
            url=item['data']['url'],
            title=item['data']['title'],
            description=item['data']['abstractNote'],
            tags=item['data']['tags'] + ['zotero-to-capacities'],
            author=item['data']['creators'][0]['firstName'] + " " + item['data']['creators'][0]['lastName'],
            zotero_link = item['links']['alternate']['href']
        )
        add_processed_key(item_key)
        process_count += 1
        if process_count >= ITEMS_PER_RUN:
            logger.info(f"Processed {process_count} items, stopping for now.")
            break


if __name__ == "__main__":
    main()