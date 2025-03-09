#!/usr/bin/env python3
"""
Main entry point for the image processor application.
"""

import argparse
import logging
import sys
import os

# Add the parent directory to the path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.image_processor import ImageProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Main function to parse arguments and run the processor."""
    parser = argparse.ArgumentParser(description='Process images with various transformations.')
    parser.add_argument('--input', '-i', default='./data/images', 
                        help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./data/output',
                        help='Directory for processed images')
    
    args = parser.parse_args()
    
    processor = ImageProcessor(args.input, args.output)
    processor.process_all_images()


if __name__ == "__main__":
    main()