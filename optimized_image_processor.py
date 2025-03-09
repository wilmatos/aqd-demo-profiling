#!/usr/bin/env python3
"""
Image Processing Pipeline - Optimized Version

This script processes images through multiple transformations with optimized performance.
"""

import os
import time
import argparse
from PIL import Image, ImageFilter, ImageEnhance
import logging
import glob
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    A class that processes images through multiple transformations.
    This is the optimized implementation.
    """
    
    def __init__(self, input_dir, output_dir):
        """Initialize the processor with input and output directories."""
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def get_image_files(self):
        """Return a list of image files in the input directory - optimized version."""
        # Use glob pattern matching for more efficient file listing - single pass
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']
        image_files = []
        
        for ext in image_extensions:
            # Use glob to efficiently get all files of each extension type
            pattern = os.path.join(self.input_dir, ext)
            image_files.extend(glob.glob(pattern))
            
            # Also check for uppercase extensions
            pattern = os.path.join(self.input_dir, ext.upper())
            image_files.extend(glob.glob(pattern))
        
        return image_files
    
    def apply_resize(self, image, size=(800, 600)):
        """Resize an image to the specified dimensions."""
        # Optimized: Using better quality resize method and no unnecessary copies
        return image.resize(size, Image.LANCZOS)  # LANCZOS is higher quality than NEAREST
    
    def apply_blur(self, image, radius=2):
        """Apply a blur filter to the image."""
        # Optimized: No unnecessary copy
        return image.filter(ImageFilter.GaussianBlur(radius))
    
    def apply_sharpen(self, image, factor=2.0):
        """Sharpen the image."""
        # Optimized: No unnecessary copy
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    def apply_contrast(self, image, factor=1.5):
        """Adjust the contrast of the image."""
        # Optimized: No unnecessary copy
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    def apply_brightness(self, image, factor=1.2):
        """Adjust the brightness of the image."""
        # Optimized: No unnecessary copy
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    def process_image(self, image_path):
        """Process a single image through the pipeline."""
        try:
            filename = os.path.basename(image_path)
            output_path = os.path.join(self.output_dir, f"processed_{filename}")
            
            logger.info(f"Processing {filename}...")
            
            # Add error handling for image loading
            try:
                image = Image.open(image_path)
            except Exception as e:
                logger.error(f"Error opening {image_path}: {e}")
                return 0
            
            # Process the image
            start_time = time.time()
            
            # Apply transformations without unnecessary copies
            image = self.apply_resize(image)
            image = self.apply_blur(image)
            image = self.apply_sharpen(image)
            image = self.apply_contrast(image)
            image = self.apply_brightness(image)
            
            # Only convert to RGB if needed
            if image.mode != 'RGB' and image_path.lower().endswith(('.jpg', '.jpeg')):
                image = image.convert('RGB')
            
            # Adjust quality based on format for better efficiency
            save_quality = 85  # Reduced from 95 - still good quality but more efficient
            save_options = {}
            
            # Format-specific saving options
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                save_options['quality'] = save_quality
                save_options['optimize'] = True
            elif output_path.lower().endswith('.png'):
                save_options['optimize'] = True
                save_options['compress_level'] = 6  # Balanced compression
            
            # Save the processed image with appropriate options
            image.save(output_path, **save_options)
            
            elapsed = time.time() - start_time
            logger.info(f"Finished processing {filename} in {elapsed:.2f} seconds")
            
            return elapsed
        except Exception as e:
            logger.error(f"Error processing {os.path.basename(image_path)}: {e}")
            return 0
    
    def process_all_images(self):
        """Process all images in the input directory with parallel processing."""
        image_files = self.get_image_files()
        
        if not image_files:
            logger.warning(f"No image files found in {self.input_dir}")
            return
        
        logger.info(f"Found {len(image_files)} images to process")
        
        total_start_time = time.time()
        
        # Determine the optimal number of workers (avoid too many or too few)
        import multiprocessing
        max_workers = min(multiprocessing.cpu_count(), len(image_files))
        workers = max(1, max_workers)  # At least 1 worker
        
        processing_times = []
        
        # Process images in parallel using process pool
        with ProcessPoolExecutor(max_workers=workers) as executor:
            # Submit all tasks
            future_to_file = {executor.submit(self.process_image, image_file): image_file 
                             for image_file in image_files}
            
            # Process results as they complete
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    elapsed = future.result()
                    if elapsed > 0:  # Only count successful processing
                        processing_times.append(elapsed)
                except Exception as e:
                    logger.error(f"Exception processing {os.path.basename(file)}: {e}")
        
        total_elapsed = time.time() - total_start_time
        
        # Calculate statistics
        if processing_times:
            avg_time = sum(processing_times) / len(processing_times)
            logger.info(f"Processed {len(processing_times)} images in {total_elapsed:.2f} seconds")
            logger.info(f"Average processing time per image: {avg_time:.2f} seconds")
            logger.info(f"Total speedup: {len(processing_times) * avg_time / total_elapsed:.2f}x theoretical sequential time")
        else:
            logger.warning("No images were processed successfully")

def main():
    """Main function to parse arguments and start processing."""
    parser = argparse.ArgumentParser(description='Process images with optimized performance.')
    parser.add_argument('--input', '-i', default='./images', help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./output', help='Directory for processed images')
    
    args = parser.parse_args()
    
    processor = ImageProcessor(args.input, args.output)
    processor.process_all_images()

if __name__ == "__main__":
    main()