#!/usr/bin/env python3
"""
Stress test for the image processor application.
This script runs the image processor with more images and more intensive processing.
"""

import os
import time
import argparse
import logging
from PIL import Image, ImageFilter, ImageEnhance
from image_processor import ImageProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StressTestProcessor(ImageProcessor):
    """
    Extended version of ImageProcessor with more intensive operations
    to stress test performance.
    """
    
    def __init__(self, input_dir, output_dir, iterations=3, blur_radius=5):
        """Initialize with additional stress test parameters."""
        super().__init__(input_dir, output_dir)
        self.iterations = iterations  # Number of times to repeat each operation
        self.blur_radius = blur_radius  # Higher blur radius for more intensive processing
    
    def apply_resize(self, image, sizes=None):
        """Resize an image multiple times with different dimensions."""
        if sizes is None:
            sizes = [(800, 600), (1024, 768), (640, 480), (1280, 720), (800, 600)]
        
        # Resize multiple times (inefficient on purpose)
        temp_image = image.copy()
        for _ in range(self.iterations):
            for size in sizes[:self.iterations]:
                temp_image = temp_image.resize(size, Image.NEAREST)
        
        # Return to original target size
        return temp_image.resize((800, 600), Image.NEAREST)
    
    def apply_blur(self, image, radius=None):
        """Apply multiple blur filters with increasing radius."""
        if radius is None:
            radius = self.blur_radius
        
        # Apply blur multiple times with increasing radius
        temp_image = image.copy()
        for i in range(self.iterations):
            current_radius = radius * (i + 1) / self.iterations
            temp_image = temp_image.filter(ImageFilter.GaussianBlur(current_radius))
        
        return temp_image
    
    def apply_sharpen(self, image, factors=None):
        """Apply multiple sharpen operations."""
        if factors is None:
            factors = [1.5, 2.0, 2.5]
        
        temp_image = image.copy()
        for _ in range(self.iterations):
            for factor in factors[:self.iterations]:
                enhancer = ImageEnhance.Sharpness(temp_image)
                temp_image = enhancer.enhance(factor)
        
        return temp_image
    
    def apply_contrast(self, image, factors=None):
        """Apply multiple contrast adjustments."""
        if factors is None:
            factors = [1.2, 1.5, 1.8]
        
        temp_image = image.copy()
        for _ in range(self.iterations):
            for factor in factors[:self.iterations]:
                enhancer = ImageEnhance.Contrast(temp_image)
                temp_image = enhancer.enhance(factor)
        
        return temp_image
    
    def apply_brightness(self, image, factors=None):
        """Apply multiple brightness adjustments."""
        if factors is None:
            factors = [1.1, 1.2, 1.3]
        
        temp_image = image.copy()
        for _ in range(self.iterations):
            for factor in factors[:self.iterations]:
                enhancer = ImageEnhance.Brightness(temp_image)
                temp_image = enhancer.enhance(factor)
        
        return temp_image
    
    def apply_additional_filters(self, image):
        """Apply additional filters to make processing more intensive."""
        temp_image = image.copy()
        
        # Apply a series of filters
        filters = [
            ImageFilter.EMBOSS,
            ImageFilter.FIND_EDGES,
            ImageFilter.CONTOUR,
            ImageFilter.EDGE_ENHANCE,
            ImageFilter.SMOOTH
        ]
        
        for _ in range(self.iterations):
            for filter_type in filters[:self.iterations]:
                temp_image = temp_image.filter(filter_type)
        
        return temp_image
    
    def process_image(self, image_path):
        """Process a single image through the extended pipeline."""
        filename = os.path.basename(image_path)
        output_path = os.path.join(self.output_dir, f"stress_processed_{filename}")
        
        logger.info(f"Processing {filename}...")
        
        try:
            # Load image
            image = Image.open(image_path)
            
            # Process start time
            start_time = time.time()
            
            # Apply transformations with multiple iterations
            image = self.apply_resize(image)
            image = self.apply_blur(image)
            image = self.apply_sharpen(image)
            image = self.apply_contrast(image)
            image = self.apply_brightness(image)
            image = self.apply_additional_filters(image)
            
            # Convert if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save with high quality
            image.save(output_path, quality=95)
            
            elapsed = time.time() - start_time
            logger.info(f"Finished processing {filename} in {elapsed:.2f} seconds")
            
            return elapsed
            
        except Exception as e:
            logger.error(f"Error processing {filename}: {e}")
            return 0

def duplicate_images(input_dir, count=20):
    """
    Duplicate existing images to create a larger dataset for stress testing.
    Returns the number of images available after duplication.
    """
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        for file in os.listdir(input_dir):
            if file.lower().endswith(ext):
                image_files.append(os.path.join(input_dir, file))
    
    if not image_files:
        logger.error(f"No images found in {input_dir}")
        return 0
    
    # Duplicate images if we don't have enough
    original_count = len(image_files)
    if original_count < count:
        logger.info(f"Duplicating images to create {count} test files...")
        for i in range(original_count, count):
            # Select a source image to duplicate
            source_image = image_files[i % original_count]
            source_name = os.path.basename(source_image)
            base, ext = os.path.splitext(source_name)
            
            # Create a new filename
            new_name = f"dup_{i+1:03d}_{base}{ext}"
            new_path = os.path.join(input_dir, new_name)
            
            # Copy the image
            try:
                img = Image.open(source_image)
                img.save(new_path)
                logger.info(f"Created duplicate: {new_name}")
            except Exception as e:
                logger.error(f"Error duplicating image {source_name}: {e}")
    
    # Count images after duplication
    image_count = 0
    for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        for file in os.listdir(input_dir):
            if file.lower().endswith(ext):
                image_count += 1
    
    return image_count

def main():
    """Main function to parse arguments and run the stress test."""
    parser = argparse.ArgumentParser(description='Stress test the image processor application.')
    parser.add_argument('--input', '-i', default='./images', 
                        help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./output',
                        help='Directory for processed images')
    parser.add_argument('--iterations', '-n', type=int, default=3,
                        help='Number of iterations for each operation')
    parser.add_argument('--blur-radius', '-b', type=int, default=5,
                        help='Maximum blur radius to use')
    parser.add_argument('--image-count', '-c', type=int, default=20,
                        help='Target number of images to process')
    
    args = parser.parse_args()
    
    # Ensure we have enough images
    image_count = duplicate_images(args.input, args.image_count)
    logger.info(f"Found/created {image_count} images for processing")
    
    # Create and run the stress test processor
    processor = StressTestProcessor(
        args.input, 
        args.output, 
        iterations=args.iterations,
        blur_radius=args.blur_radius
    )
    
    logger.info(f"Starting stress test with {args.iterations} iterations per operation...")
    start_time = time.time()
    processor.process_all_images()
    total_time = time.time() - start_time
    
    logger.info(f"Stress test completed in {total_time:.2f} seconds")
    logger.info(f"Processed {image_count} images with {args.iterations} iterations each")

if __name__ == "__main__":
    main()