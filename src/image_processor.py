#!/usr/bin/env python3
"""
Image Processing Pipeline - Optimized Version

This module provides a class for processing images through multiple transformations efficiently.
"""

import os
import time
import logging
from PIL import Image, ImageFilter, ImageEnhance
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

from src.utils.file_utils import get_image_files, ensure_directory

# Configure logging
logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    A class that processes images through multiple transformations efficiently.
    """
    
    def __init__(self, input_dir, output_dir):
        """
        Initialize the processor with input and output directories.
        
        Args:
            input_dir (str): Directory containing input images
            output_dir (str): Directory for processed images
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Determine the number of processes to use (leave one core free)
        self.num_workers = max(1, multiprocessing.cpu_count() - 1)
        
        # Create output directory if it doesn't exist
        ensure_directory(self.output_dir)
    
    def apply_resize(self, image, size=(800, 600)):
        """
        Resize an image to the specified dimensions.
        
        Args:
            image (PIL.Image): Image to resize
            size (tuple): Target dimensions (width, height)
            
        Returns:
            PIL.Image: Resized image
        """
        return image.resize(size, Image.LANCZOS)
    
    def apply_blur(self, image, radius=2):
        """
        Apply a blur filter to the image.
        
        Args:
            image (PIL.Image): Image to blur
            radius (int): Blur radius
            
        Returns:
            PIL.Image: Blurred image
        """
        return image.filter(ImageFilter.GaussianBlur(radius))
    
    def apply_sharpen(self, image, factor=2.0):
        """
        Sharpen the image.
        
        Args:
            image (PIL.Image): Image to sharpen
            factor (float): Sharpness enhancement factor
            
        Returns:
            PIL.Image: Sharpened image
        """
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    def apply_contrast(self, image, factor=1.5):
        """
        Adjust the contrast of the image.
        
        Args:
            image (PIL.Image): Image to adjust
            factor (float): Contrast enhancement factor
            
        Returns:
            PIL.Image: Contrast-adjusted image
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    def apply_brightness(self, image, factor=1.2):
        """
        Adjust the brightness of the image.
        
        Args:
            image (PIL.Image): Image to adjust
            factor (float): Brightness enhancement factor
            
        Returns:
            PIL.Image: Brightness-adjusted image
        """
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    def process_image(self, image_path):
        """
        Process a single image through the pipeline.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            float: Processing time in seconds, or 0 if processing failed
        """
        filename = os.path.basename(image_path)
        output_path = os.path.join(self.output_dir, f"processed_{filename}")
        
        logger.info(f"Processing {filename}...")
        
        try:
            # Optimized loading - with error handling
            with Image.open(image_path) as image:
                # Start timing after successful image loading
                start_time = time.time()
                
                # Apply transformations without unnecessary copies
                image = self.apply_resize(image)
                image = self.apply_blur(image)
                image = self.apply_sharpen(image)
                image = self.apply_contrast(image)
                image = self.apply_brightness(image)
                
                # Only convert to RGB if needed for JPEG or specific formats that require it
                ext = os.path.splitext(output_path)[1].lower()
                if ext in {'.jpg', '.jpeg'} and image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Save with balanced quality setting (80 is a good balance between quality and file size)
                image.save(output_path, quality=80)
                
                elapsed = time.time() - start_time
                logger.info(f"Finished processing {filename} in {elapsed:.2f} seconds")
                
                return elapsed
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}")
            return 0
    
    def process_all_images(self):
        """
        Process all images in the input directory using parallel processing.
        
        Returns:
            tuple: (successful_count, total_count, avg_time, total_elapsed)
        """
        image_files = get_image_files(self.input_dir)
        
        if not image_files:
            logger.warning(f"No image files found in {self.input_dir}")
            return (0, 0, 0, 0)
        
        num_images = len(image_files)
        logger.info(f"Found {num_images} images to process using {self.num_workers} worker processes")
        
        total_start_time = time.time()
        
        # Optimized - parallel processing using ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            try:
                # Submit all tasks and collect results
                future_to_file = {executor.submit(self.process_image, image_file): image_file 
                                 for image_file in image_files}
                
                # Process results as they complete
                processing_times = []
                for future in future_to_file:
                    try:
                        processing_time = future.result()
                        if processing_time > 0:  # Only count successful operations
                            processing_times.append(processing_time)
                    except Exception as exc:
                        file = future_to_file[future]
                        logger.error(f"Generated an exception during parallel processing: {file}, {exc}")
                
                # Calculate statistics
                successful_count = len(processing_times)
                total_processing_time = sum(processing_times)
                avg_time = total_processing_time / successful_count if successful_count > 0 else 0
                
            except Exception as e:
                logger.error(f"Error in parallel processing: {str(e)}")
                successful_count = 0
                avg_time = 0
        
        total_elapsed = time.time() - total_start_time
        
        logger.info(f"Processed {successful_count} of {num_images} images in {total_elapsed:.2f} seconds "
                  f"(average: {avg_time:.2f} seconds per image)")
        
        return (successful_count, num_images, avg_time, total_elapsed)