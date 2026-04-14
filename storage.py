import json
import os

STORAGE_FILE = "storage.json"

def load_seen():
    """Load the list of already seen job links from JSON file."""
    if not os.path.exists(STORAGE_FILE):
        return set()
    try:
        with open(STORAGE_FILE, 'r') as f:
            data = json.load(f)
            return set(data)
    except (json.JSONDecodeError, TypeError):
        return set()

def save_seen(seen_links):
    """Save the list of seen job links to JSON file."""
    with open(STORAGE_FILE, 'w') as f:
        json.dump(list(seen_links), f, indent=4)
