#!/usr/bin/env python3
"""
Unit tests for the image processor.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# Add the parent directory to the path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.image_processor import ImageProcessor


class TestImageProcessor(unittest.TestCase):
    """Test cases for the ImageProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.temp_dir, 'input')
        self.output_dir = os.path.join(self.temp_dir, 'output')
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create a test image
        self.test_image_path = os.path.join(self.input_dir, 'test.jpg')
        with open(self.test_image_path, 'w') as f:
            f.write('dummy image data')
    
    def tearDown(self):
        """Tear down test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_init(self):
        """Test initialization of ImageProcessor."""
        processor = ImageProcessor(self.input_dir, self.output_dir)
        self.assertEqual(processor.input_dir, self.input_dir)
        self.assertEqual(processor.output_dir, self.output_dir)
    
    @patch('src.image_processor.get_image_files')
    def test_process_all_images_no_images(self, mock_get_image_files):
        """Test process_all_images with no images."""
        mock_get_image_files.return_value = []
        
        processor = ImageProcessor(self.input_dir, self.output_dir)
        result = processor.process_all_images()
        
        self.assertEqual(result, (0, 0, 0, 0))
        mock_get_image_files.assert_called_once_with(self.input_dir)
    
    @patch('src.image_processor.get_image_files')
    @patch('src.image_processor.ProcessPoolExecutor')
    def test_process_all_images(self, mock_executor, mock_get_image_files):
        """Test process_all_images with mock images."""
        # Mock image files
        mock_get_image_files.return_value = [
            os.path.join(self.input_dir, 'image1.jpg'),
            os.path.join(self.input_dir, 'image2.jpg')
        ]
        
        # Mock executor
        mock_executor_instance = MagicMock()
        mock_executor.return_value.__enter__.return_value = mock_executor_instance
        
        # Mock futures
        mock_future1 = MagicMock()
        mock_future1.result.return_value = 0.5
        mock_future2 = MagicMock()
        mock_future2.result.return_value = 0.7
        
        mock_executor_instance.submit.side_effect = [mock_future1, mock_future2]
        
        # Run the method
        processor = ImageProcessor(self.input_dir, self.output_dir)
        result = processor.process_all_images()
        
        # Check results
        self.assertEqual(result[0], 2)  # successful_count
        self.assertEqual(result[1], 2)  # num_images
        self.assertAlmostEqual(result[2], 0.6)  # avg_time
        
        # Check that submit was called for each image
        self.assertEqual(mock_executor_instance.submit.call_count, 2)


if __name__ == '__main__':
    unittest.main()