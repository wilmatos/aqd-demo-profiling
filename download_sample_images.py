#!/usr/bin/env python3
"""
Script to download sample images for the image processing demo.
Downloads public domain images from Unsplash Source API.
"""

import os
import argparse
import urllib.request
import random
import time

def download_image(url, save_path):
    """Download an image from URL and save it to the specified path."""
    try:
        urllib.request.urlretrieve(url, save_path)
        print(f"Downloaded: {save_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    """Main function to download sample images."""
    parser = argparse.ArgumentParser(description='Download sample images for processing.')
    parser.add_argument('--output', '-o', default='./images',
                        help='Directory to save downloaded images')
    parser.add_argument('--count', '-c', type=int, default=10,
                        help='Number of images to download')
    parser.add_argument('--width', '-w', type=int, default=1200,
                        help='Width of images to download')
    parser.add_argument('--height', '--ht', type=int, default=800,
                        help='Height of images to download')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(args.output, exist_ok=True)
    
    # Categories for random images
    categories = ['nature', 'architecture', 'technology', 'food', 'animals', 
                  'travel', 'business', 'fashion', 'people', 'health']
    
    print(f"Downloading {args.count} sample images to {args.output}...")
    
    success_count = 0
    for i in range(args.count):
        # Select a random category
        category = random.choice(categories)
        
        # Create URL for Unsplash Source API
        url = f"https://picsum.photos/{args.width}/{args.height}"
        
        # Create save path
        save_path = os.path.join(args.output, f"sample_image_{i+1:03d}.jpg")
        
        # Download the image
        if download_image(url, save_path):
            success_count += 1
        
        # Add a small delay to avoid rate limiting
        time.sleep(0.5)
    
    print(f"Downloaded {success_count} of {args.count} images successfully.")

if __name__ == "__main__":
    main()