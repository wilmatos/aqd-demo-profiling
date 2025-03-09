#!/usr/bin/env python3
"""
Script to download sample images for testing the image processor.
"""

import os
import sys
import requests
import logging
from concurrent.futures import ThreadPoolExecutor

# Add the parent directory to the path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.file_utils import ensure_directory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Sample image URLs
SAMPLE_IMAGES = [
    "https://images.unsplash.com/photo-1501854140801-50d01698950b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1497449493050-aad1e7cad165?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1518173946395-054bfb632e9b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80"
]

def download_image(url, output_dir, index):
    """Download an image from a URL and save it to the output directory."""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        # Extract filename from URL or use a default name
        filename = f"sample_image_{index:03d}.jpg"
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"Downloaded {filename}")
        return True
    except Exception as e:
        logger.error(f"Error downloading image {index}: {str(e)}")
        return False

def main():
    """Main function to download sample images."""
    parser = argparse.ArgumentParser(description='Download sample images for testing.')
    parser.add_argument('--output', '-o', default='./data/images',
                        help='Directory to save downloaded images')
    parser.add_argument('--count', '-c', type=int, default=10,
                        help='Number of images to download (max 10)')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    ensure_directory(args.output)
    
    # Limit count to available images
    count = min(args.count, len(SAMPLE_IMAGES))
    
    logger.info(f"Downloading {count} sample images to {args.output}...")
    
    # Download images in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(download_image, SAMPLE_IMAGES[i], args.output, i+1)
            for i in range(count)
        ]
        
        # Create duplicates for stress testing
        if count >= 5:
            for i in range(5):
                for j in range(2):
                    dup_index = 10 + i*2 + j + 1
                    executor.submit(download_image, SAMPLE_IMAGES[i], args.output, dup_index)
    
    logger.info(f"Download complete. Images saved to {args.output}")

if __name__ == "__main__":
    import argparse
    main()