#!/usr/bin/env python3
"""
Profiling script for the stress test version of the image processor.
This script runs the stress test with various profiling tools.
"""

import os
import sys
import cProfile
import pstats
import time
import argparse
from memory_profiler import profile as memory_profile
from stress_test import StressTestProcessor, duplicate_images
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def cpu_profile(input_dir, output_dir, profile_output, iterations=3, blur_radius=5, image_count=20):
    """Profile the CPU usage of the stress test processor."""
    print(f"Running CPU profiling for stress test...")
    
    # Ensure we have enough images
    duplicate_images(input_dir, image_count)
    
    # Create profiler
    profiler = cProfile.Profile()
    
    # Start profiling
    profiler.enable()
    
    # Run the processor
    processor = StressTestProcessor(
        input_dir, 
        output_dir, 
        iterations=iterations,
        blur_radius=blur_radius
    )
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
    stats.print_stats(30)  # Print top 30 functions


@memory_profile
def memory_profile_run(input_dir, output_dir, iterations=3, blur_radius=5, image_count=20):
    """Run the stress test processor with memory profiling."""
    # Ensure we have enough images
    duplicate_images(input_dir, image_count)
    
    processor = StressTestProcessor(
        input_dir, 
        output_dir, 
        iterations=iterations,
        blur_radius=blur_radius
    )
    processor.process_all_images()


def run_memory_profile(input_dir, output_dir, iterations=3, blur_radius=5, image_count=20):
    """Profile the memory usage of the stress test processor."""
    print(f"Running memory profiling for stress test...")
    memory_profile_run(input_dir, output_dir, iterations, blur_radius, image_count)


def run_time_profile(input_dir, output_dir, iterations=3, blur_radius=5, image_count=20):
    """Profile the execution time of the stress test processor."""
    print(f"Running time profiling for stress test...")
    
    # Ensure we have enough images
    duplicate_images(input_dir, image_count)
    
    start_time = time.time()
    
    processor = StressTestProcessor(
        input_dir, 
        output_dir, 
        iterations=iterations,
        blur_radius=blur_radius
    )
    processor.process_all_images()
    
    elapsed = time.time() - start_time
    
    print(f"\nTime Profile Results:")
    print(f"Total execution time: {elapsed:.2f} seconds")
    print(f"Processed {image_count} images with {iterations} iterations each")


def main():
    """Main function to parse arguments and run the profiler."""
    parser = argparse.ArgumentParser(description='Profile the stress test version of the image processor.')
    parser.add_argument('--input', '-i', default='./images', 
                        help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./output',
                        help='Directory for processed images')
    parser.add_argument('--profile-type', '-p', choices=['cpu', 'memory', 'time', 'all'],
                        default='all', help='Type of profiling to run')
    parser.add_argument('--profile-output', default='./profiles/stress_profile_stats.prof',
                        help='Output file for profiling data')
    parser.add_argument('--iterations', '-n', type=int, default=3,
                        help='Number of iterations for each operation')
    parser.add_argument('--blur-radius', '-b', type=int, default=5,
                        help='Maximum blur radius to use')
    parser.add_argument('--image-count', '-c', type=int, default=20,
                        help='Target number of images to process')
    
    args = parser.parse_args()
    
    # Ensure profiles directory exists
    os.makedirs(os.path.dirname(args.profile_output), exist_ok=True)
    
    # Run the selected profiling type
    if args.profile_type in ['cpu', 'all']:
        cpu_profile(
            args.input, 
            args.output, 
            args.profile_output, 
            args.iterations, 
            args.blur_radius, 
            args.image_count
        )
    
    if args.profile_type in ['memory', 'all']:
        run_memory_profile(
            args.input, 
            args.output, 
            args.iterations, 
            args.blur_radius, 
            args.image_count
        )
    
    if args.profile_type in ['time', 'all']:
        run_time_profile(
            args.input, 
            args.output, 
            args.iterations, 
            args.blur_radius, 
            args.image_count
        )


if __name__ == "__main__":
    main()