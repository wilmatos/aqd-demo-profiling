#!/usr/bin/env python3
"""
Profiling script for the image processor application.
This script runs the image processor with various profiling tools.
"""

import os
import sys
import cProfile
import pstats
import time
import argparse
from memory_profiler import profile as memory_profile

# Add the parent directory to the path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.image_processor import ImageProcessor
from src.utils.file_utils import ensure_directory

def cpu_profile(input_dir, output_dir, profile_output):
    """Profile the CPU usage of the image processor."""
    print(f"Running CPU profiling...")
    
    # Create profiler
    profiler = cProfile.Profile()
    
    # Start profiling
    profiler.enable()
    
    # Run the processor
    processor = ImageProcessor(input_dir, output_dir)
    processor.process_all_images()
    
    # Stop profiling
    profiler.disable()
    
    # Save stats to file
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.dump_stats(profile_output)
    
    # Print stats summary
    print(f"\nCPU Profile Results (saved to {profile_output}):")
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Print top 20 functions


@memory_profile
def memory_profile_run(input_dir, output_dir):
    """Run the image processor with memory profiling."""
    processor = ImageProcessor(input_dir, output_dir)
    processor.process_all_images()


def run_memory_profile(input_dir, output_dir):
    """Profile the memory usage of the image processor."""
    print(f"Running memory profiling...")
    memory_profile_run(input_dir, output_dir)


def run_time_profile(input_dir, output_dir):
    """Profile the execution time of the image processor."""
    print(f"Running time profiling...")
    
    start_time = time.time()
    
    processor = ImageProcessor(input_dir, output_dir)
    processor.process_all_images()
    
    elapsed = time.time() - start_time
    
    print(f"\nTime Profile Results:")
    print(f"Total execution time: {elapsed:.2f} seconds")


def main():
    """Main function to parse arguments and run the profiler."""
    parser = argparse.ArgumentParser(description='Profile the image processor application.')
    parser.add_argument('--input', '-i', default='./data/images', 
                        help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./data/output',
                        help='Directory for processed images')
    parser.add_argument('--profile-type', '-p', choices=['cpu', 'memory', 'time', 'all'],
                        default='all', help='Type of profiling to run')
    parser.add_argument('--profile-output', default='./profiling/reports/profile_stats.prof',
                        help='Output file for profiling data')
    
    args = parser.parse_args()
    
    # Ensure profiles directory exists
    ensure_directory(os.path.dirname(args.profile_output))
    
    # Run the selected profiling type
    if args.profile_type in ['cpu', 'all']:
        cpu_profile(args.input, args.output, args.profile_output)
    
    if args.profile_type in ['memory', 'all']:
        run_memory_profile(args.input, args.output)
    
    if args.profile_type in ['time', 'all']:
        run_time_profile(args.input, args.output)


if __name__ == "__main__":
    main()