"""
File utility functions for the image processor.
"""

import os
import logging

logger = logging.getLogger(__name__)

def get_image_files(directory):
    """
    Return a list of image files in the specified directory using a single pass.
    
    Args:
        directory (str): Path to the directory containing image files
        
    Returns:
        list: List of full paths to image files
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}  # Using set for faster lookups
    image_files = []
    
    try:
        # Optimized way - walks through all files just once
        for file in os.listdir(directory):
            ext = os.path.splitext(file.lower())[1]
            if ext in image_extensions:
                image_files.append(os.path.join(directory, file))
    except Exception as e:
        logger.error(f"Error listing files in {directory}: {str(e)}")
    
    return image_files


def ensure_directory(directory):
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory (str): Path to the directory to ensure exists
    """
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}")
        raise