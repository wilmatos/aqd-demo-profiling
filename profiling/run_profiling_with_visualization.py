#!/usr/bin/env python3
"""
Run profiling and generate visualizations in one step.
"""

import os
import sys
import argparse
import subprocess

# Add the parent directory to the path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.file_utils import ensure_directory

def run_profiling_and_visualization(input_dir, output_dir, profile_output, visualization_output):
    """
    Run profiling and generate visualization.
    
    Args:
        input_dir (str): Directory containing input images
        output_dir (str): Directory for processed images
        profile_output (str): Path to save profile stats
        visualization_output (str): Path to save visualization image
    """
    # Ensure directories exist
    ensure_directory(os.path.dirname(profile_output))
    ensure_directory(os.path.dirname(visualization_output))
    
    # Step 1: Run profiling
    print("Step 1: Running profiling...")
    profile_script = os.path.join(os.path.dirname(__file__), 'profile_processor.py')
    subprocess.run([
        'python', profile_script,
        '--input', input_dir,
        '--output', output_dir,
        '--profile-type', 'cpu',
        '--profile-output', profile_output
    ], check=True)
    
    # Step 2: Generate visualization
    print("\nStep 2: Generating visualization...")
    visualize_script = os.path.join(os.path.dirname(__file__), 'visualize_profile.py')
    subprocess.run([
        'python', visualize_script,
        '--profile', profile_output,
        '--output', visualization_output
    ], check=True)
    
    print("\nProfiling and visualization complete!")
    print(f"Profile stats: {profile_output}")
    print(f"Visualization: {visualization_output}")


def main():
    """Main function to parse arguments and run profiling with visualization."""
    parser = argparse.ArgumentParser(description='Run profiling and generate visualizations.')
    parser.add_argument('--input', '-i', default='./data/images',
                        help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./data/output',
                        help='Directory for processed images')
    parser.add_argument('--profile-output', default='./profiling/reports/profile_stats.prof',
                        help='Path to save profile stats')
    parser.add_argument('--visualization-output', default='./profiling/reports/profile_visualization.png',
                        help='Path to save visualization image')
    
    args = parser.parse_args()
    
    run_profiling_and_visualization(
        args.input,
        args.output,
        args.profile_output,
        args.visualization_output
    )


if __name__ == "__main__":
    main()