import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram configurations
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# List of keywords/interests for AI filtering
KEYWORDS = [
    "cybersecurity intern",
    "cyber security intern",
    "security analyst intern",
    "soc analyst intern",
    "monitoring analyst intern",
    "threat analyst intern",
    "information security intern",
    "network security intern",
    "security operations intern",
    "vulnerability intern"
]

# AI Filtering settings
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.6))

# Scraper Settings
REQUEST_TIMEOUT = 15
SCRAPE_INTERVAL_MINUTES = int(os.getenv("SCRAPE_INTERVAL_MINUTES", 10))
