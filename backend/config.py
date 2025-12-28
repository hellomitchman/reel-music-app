"""Configuration settings for the Reel Music App"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# File settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv"}

# Music generation settings
# You'll need to get a free API key from https://mubert.com/render/api
MUBERT_LICENSE = os.getenv("MUBERT_LICENSE", "")  # Get from environment variable

# Supported music styles/moods
MUSIC_STYLES = [
    "ambient", "chill", "corporate", "dramatic", "energetic",
    "epic", "happy", "inspiring", "romantic", "sad", "upbeat"
]
