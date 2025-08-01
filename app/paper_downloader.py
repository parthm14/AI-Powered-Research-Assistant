# app/paper_downloader.py

import os
import requests
from urllib.parse import urlparse
from app.config import PAPER_STORAGE_DIR

def sanitize_filename(url: str) -> str:
    """
    Generates a safe filename from the URL by extracting and cleaning the path.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename.endswith(".pdf"):
        filename += ".pdf"
    return filename.replace(" ", "_")

def download_pdf(url: str, storage_dir: str = PAPER_STORAGE_DIR) -> str:
    """
    Downloads a PDF from the given URL and saves it to the specified storage directory.

    Args:
        url (str): The URL to download the PDF from.
        storage_dir (str): Directory to save the PDF.

    Returns:
        str: Full path to the saved file, or None if download fails.
    """
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)

    filename = sanitize_filename(url)
    file_path = os.path.join(storage_dir, filename)

    try:
        response = requests.get(url, stream=True, timeout=20)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None