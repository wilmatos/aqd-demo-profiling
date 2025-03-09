#!/usr/bin/env python3
"""
Profile the stress test for the image processor.
"""

import os
import sys
import cProfile
import pstats
import argparse
import logging

# Add the parent directory to the path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.stress_test import run_stress_test
from src.utils.file_utils import ensure_directory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def profile_stress_test(input_dir, output_dir, iterations, profile_output):
    """
    Profile the stress test.
    
    Args:
        input_dir (str): Directory containing input images
        output_dir (str): Directory for processed images
        iterations (int): Number of iterations to run
        profile_output (str): Path to save profile stats
    """
    # Ensure output directory exists
    ensure_directory(os.path.dirname(profile_output))
    
    logger.info(f"Profiling stress test with {iterations} iterations...")
    
    # Create profiler
    profiler = cProfile.Profile()
    
    # Start profiling
    profiler.enable()
    
    # Run the stress test
    total_time, avg_time, total_images = run_stress_test(input_dir, output_dir, iterations)
    
    # Stop profiling
    profiler.disable()
    
    # Save stats to file
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.dump_stats(profile_output)
    
    # Print stats summary
    logger.info(f"\nStress Test Profile Results (saved to {profile_output}):")
    logger.info(f"Total time: {total_time:.2f} seconds")
    logger.info(f"Average time per image: {avg_time:.4f} seconds")
    logger.info(f"Total images processed: {total_images * iterations}")
    
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Print top 20 functions


def main():
    """Main function to parse arguments and run the profiled stress test."""
    parser = argparse.ArgumentParser(description='Profile the stress test for the image processor.')
    parser.add_argument('--input', '-i', default='./data/images',
                        help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./data/output',
                        help='Directory for processed images')
    parser.add_argument('--iterations', '-n', type=int, default=3,
                        help='Number of iterations to run')
    parser.add_argument('--profile-output', default='./profiling/reports/stress_test_profile.prof',
                        help='Path to save profile stats')
    
    args = parser.parse_args()
    
    profile_stress_test(
        args.input,
        args.output,
        args.iterations,
        args.profile_output
    )


if __name__ == "__main__":
    main()