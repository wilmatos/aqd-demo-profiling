#!/usr/bin/env python3
"""
Stress test for the image processor.
This script runs the image processor with a large number of images and iterations.
"""

import os
import sys
import time
import argparse
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor

# Add the parent directory to the path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.image_processor import ImageProcessor
from src.utils.file_utils import ensure_directory, get_image_files

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def duplicate_images(source_dir, target_dir, count):
    """
    Duplicate images from source directory to target directory.
    
    Args:
        source_dir (str): Directory containing source images
        target_dir (str): Directory to save duplicated images
        count (int): Number of duplicates to create for each image
        
    Returns:
        int: Number of images created
    """
    # Ensure target directory exists
    ensure_directory(target_dir)
    
    # Get source images
    source_images = get_image_files(source_dir)
    if not source_images:
        logger.error(f"No images found in {source_dir}")
        return 0
    
    logger.info(f"Found {len(source_images)} source images")
    
    # Create duplicates
    created_count = 0
    
    def copy_image(src, index):
        try:
            filename = os.path.basename(src)
            name, ext = os.path.splitext(filename)
            dst = os.path.join(target_dir, f"dup_{index:03d}_{filename}")
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            logger.error(f"Error duplicating image {src}: {str(e)}")
            return False
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        index = 1
        
        for _ in range(count):
            for src in source_images:
                futures.append(executor.submit(copy_image, src, index))
                index += 1
        
        for future in futures:
            if future.result():
                created_count += 1
    
    logger.info(f"Created {created_count} duplicate images in {target_dir}")
    return created_count


def run_stress_test(input_dir, output_dir, iterations=3):
    """
    Run a stress test on the image processor.
    
    Args:
        input_dir (str): Directory containing input images
        output_dir (str): Directory for processed images
        iterations (int): Number of iterations to run
        
    Returns:
        tuple: (total_time, avg_time_per_image, total_images)
    """
    # Ensure output directory exists and is empty
    ensure_directory(output_dir)
    for item in os.listdir(output_dir):
        item_path = os.path.join(output_dir, item)
        if os.path.isfile(item_path):
            os.unlink(item_path)
    
    # Count input images
    image_files = get_image_files(input_dir)
    total_images = len(image_files)
    
    if total_images == 0:
        logger.error(f"No images found in {input_dir}")
        return (0, 0, 0)
    
    logger.info(f"Starting stress test with {total_images} images, {iterations} iterations")
    
    # Run the processor multiple times
    total_start_time = time.time()
    
    processor = ImageProcessor(input_dir, output_dir)
    
    for i in range(iterations):
        logger.info(f"Iteration {i+1}/{iterations}")
        processor.process_all_images()
    
    total_time = time.time() - total_start_time
    avg_time_per_image = total_time / (total_images * iterations)
    
    logger.info(f"Stress test completed in {total_time:.2f} seconds")
    logger.info(f"Processed {total_images} images {iterations} times")
    logger.info(f"Average time per image: {avg_time_per_image:.4f} seconds")
    
    return (total_time, avg_time_per_image, total_images)


def main():
    """Main function to parse arguments and run the stress test."""
    parser = argparse.ArgumentParser(description='Run a stress test on the image processor.')
    parser.add_argument('--input', '-i', default='./data/images',
                        help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./data/output',
                        help='Directory for processed images')
    parser.add_argument('--iterations', '-n', type=int, default=3,
                        help='Number of iterations to run')
    parser.add_argument('--duplicate', '-d', type=int, default=0,
                        help='Number of duplicates to create for each image')
    parser.add_argument('--duplicate-dir', default='./data/images/duplicates',
                        help='Directory to store duplicated images')
    
    args = parser.parse_args()
    
    # Create duplicates if requested
    if args.duplicate > 0:
        duplicate_images(args.input, args.duplicate_dir, args.duplicate)
        input_dir = args.duplicate_dir
    else:
        input_dir = args.input
    
    # Run the stress test
    run_stress_test(input_dir, args.output, args.iterations)


if __name__ == "__main__":
    main()