#!/usr/bin/env python3
"""
Script to run profiling and automatically visualize the results with KCachegrind.
"""

import os
import sys
import argparse
import subprocess
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_profiling_and_visualize(profile_type='cpu', stress_test=False, 
                               input_dir='./images', output_dir='./output',
                               iterations=3, image_count=10):
    """
    Run profiling and visualize the results with KCachegrind.
    
    Args:
        profile_type: Type of profiling to run ('cpu', 'memory', 'time', 'all')
        stress_test: Whether to run the stress test version
        input_dir: Directory containing input images
        output_dir: Directory for processed images
        iterations: Number of iterations for stress test
        image_count: Target number of images for stress test
    """
    # Ensure profiles directory exists
    os.makedirs('./profiles', exist_ok=True)
    
    # Determine which profiling script to run
    script = 'profile_stress_test.py' if stress_test else 'profile_processor.py'
    profile_file = './profiles/stress_profile_stats.prof' if stress_test else './profiles/profile_stats.prof'
    
    # Build the command
    cmd = [
        'python', script,
        '--input', input_dir,
        '--output', output_dir,
        '--profile-type', profile_type
    ]
    
    # Add stress test specific arguments
    if stress_test:
        cmd.extend([
            '--iterations', str(iterations),
            '--image-count', str(image_count)
        ])
    
    # Run the profiling
    logger.info(f"Running {'stress test' if stress_test else 'regular'} profiling with {profile_type} profile type...")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running profiling: {e}")
        return False
    
    # Only visualize CPU profiling
    if profile_type in ['cpu', 'all']:
        # Wait a moment to ensure the profile file is written
        time.sleep(1)
        
        # Convert and open with KCachegrind
        logger.info("Converting profile data and opening KCachegrind...")
        try:
            subprocess.run(['python', 'visualize_profile.py', profile_file], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error visualizing profile: {e}")
            return False
    else:
        logger.info(f"Skipping visualization for {profile_type} profiling (only CPU profiles can be visualized with KCachegrind)")
    
    return True

def main():
    """Parse command line arguments and run profiling with visualization."""
    parser = argparse.ArgumentParser(
        description='Run profiling and visualize results with KCachegrind.'
    )
    parser.add_argument('--profile-type', '-p', choices=['cpu', 'memory', 'time', 'all'],
                        default='cpu', help='Type of profiling to run')
    parser.add_argument('--stress-test', '-s', action='store_true',
                        help='Run the stress test version')
    parser.add_argument('--input', '-i', default='./images',
                        help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./output',
                        help='Directory for processed images')
    parser.add_argument('--iterations', '-n', type=int, default=3,
                        help='Number of iterations for stress test')
    parser.add_argument('--image-count', '-c', type=int, default=10,
                        help='Target number of images for stress test')
    
    args = parser.parse_args()
    
    run_profiling_and_visualize(
        args.profile_type,
        args.stress_test,
        args.input,
        args.output,
        args.iterations,
        args.image_count
    )

if __name__ == "__main__":
    main()