#!/usr/bin/env python3
"""
Image Processing Pipeline

This script processes images through multiple transformations in an intentionally
inefficient way to demonstrate performance optimization opportunities.
"""

import os
import time
import argparse
from PIL import Image, ImageFilter, ImageEnhance
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    A class that processes images through multiple transformations.
    Initial implementation is intentionally inefficient.
    """
    
    def __init__(self, input_dir, output_dir):
        """Initialize the processor with input and output directories."""
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def get_image_files(self):
        """Return a list of image files in the input directory."""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        image_files = []
        
        # Inefficient way to list files - walks through all files multiple times
        for ext in image_extensions:
            for file in os.listdir(self.input_dir):
                if file.lower().endswith(ext):
                    image_files.append(os.path.join(self.input_dir, file))
        
        return image_files
    
    def apply_resize(self, image, size=(800, 600)):
        """Resize an image to the specified dimensions."""
        # Inefficient implementation - creates unnecessary intermediate objects
        temp_image = image.copy()
        resized = temp_image.resize(size, Image.NEAREST)  # Using NEAREST instead of better quality methods
        return resized
    
    def apply_blur(self, image, radius=2):
        """Apply a blur filter to the image."""
        # Inefficient - creates a new copy and applies a simple blur
        temp_image = image.copy()
        return temp_image.filter(ImageFilter.GaussianBlur(radius))
    
    def apply_sharpen(self, image, factor=2.0):
        """Sharpen the image."""
        # Inefficient - creates a new copy for each operation
        temp_image = image.copy()
        enhancer = ImageEnhance.Sharpness(temp_image)
        return enhancer.enhance(factor)
    
    def apply_contrast(self, image, factor=1.5):
        """Adjust the contrast of the image."""
        # Inefficient - creates a new copy for each operation
        temp_image = image.copy()
        enhancer = ImageEnhance.Contrast(temp_image)
        return enhancer.enhance(factor)
    
    def apply_brightness(self, image, factor=1.2):
        """Adjust the brightness of the image."""
        # Inefficient - creates a new copy for each operation
        temp_image = image.copy()
        enhancer = ImageEnhance.Brightness(temp_image)
        return enhancer.enhance(factor)
    
    def process_image(self, image_path):
        """Process a single image through the pipeline."""
        filename = os.path.basename(image_path)
        output_path = os.path.join(self.output_dir, f"processed_{filename}")
        
        logger.info(f"Processing {filename}...")
        
        # Inefficient loading - no error handling
        image = Image.open(image_path)
        
        # Inefficient processing - sequential operations with unnecessary copies
        start_time = time.time()
        
        # Apply transformations one by one, creating new copies each time
        image = self.apply_resize(image)
        image = self.apply_blur(image)
        image = self.apply_sharpen(image)
        image = self.apply_contrast(image)
        image = self.apply_brightness(image)
        
        # Inefficient - unnecessary conversion
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save the processed image
        image.save(output_path, quality=95)  # High quality setting is inefficient
        
        elapsed = time.time() - start_time
        logger.info(f"Finished processing {filename} in {elapsed:.2f} seconds")
        
        return elapsed
    
    def process_all_images(self):
        """Process all images in the input directory."""
        image_files = self.get_image_files()
        
        if not image_files:
            logger.warning(f"No image files found in {self.input_dir}")
            return
        
        logger.info(f"Found {len(image_files)} images to process")
        
        total_start_time = time.time()
        
        # Process images sequentially - no parallelism
        processing_times = []
        for image_file in image_files:
            elapsed = self.process_image(image_file)
            processing_times.append(elapsed)
        
        total_elapsed = time.time() - total_start_time
        
        # Calculate statistics
        avg_time = sum(processing_times) / len(processing_times) if processing_times else 0
        
        logger.info(f"Processed {len(image_files)} images in {total_elapsed:.2f} seconds")
        logger.info(f"Average processing time per image: {avg_time:.2f} seconds")


def main():
    """Main function to parse arguments and run the processor."""
    parser = argparse.ArgumentParser(description='Process images with various transformations.')
    parser.add_argument('--input', '-i', default='./images', 
                        help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./output',
                        help='Directory for processed images')
    
    args = parser.parse_args()
    
    processor = ImageProcessor(args.input, args.output)
    processor.process_all_images()


if __name__ == "__main__":
    main()