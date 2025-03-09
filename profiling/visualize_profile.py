#!/usr/bin/env python3
"""
Visualize profiling results from the image processor.
"""

import os
import sys
import argparse
import pstats
import gprof2dot
import subprocess

# Add the parent directory to the path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.file_utils import ensure_directory

def visualize_profile(profile_file, output_file):
    """
    Convert a profile file to a graphical representation.
    
    Args:
        profile_file (str): Path to the profile stats file
        output_file (str): Path to save the output image
    """
    try:
        # Ensure the output directory exists
        ensure_directory(os.path.dirname(output_file))
        
        # Generate DOT file
        dot_file = f"{os.path.splitext(output_file)[0]}.dot"
        
        # Use gprof2dot to convert profile to DOT format
        stats = pstats.Stats(profile_file)
        with open(dot_file, 'w') as f:
            gprof2dot.main([
                '-f', 'pstats', 
                profile_file, 
                '-o', dot_file
            ])
        
        # Convert DOT to PNG using graphviz
        subprocess.run(['dot', '-Tpng', dot_file, '-o', output_file], check=True)
        
        print(f"Profile visualization saved to {output_file}")
        
    except Exception as e:
        print(f"Error visualizing profile: {str(e)}")
        return False
    
    return True


def main():
    """Main function to parse arguments and visualize profile."""
    parser = argparse.ArgumentParser(description='Visualize profiling results.')
    parser.add_argument('--profile', '-p', default='./profiling/reports/profile_stats.prof',
                        help='Path to the profile stats file')
    parser.add_argument('--output', '-o', default='./profiling/reports/profile_visualization.png',
                        help='Path to save the visualization image')
    
    args = parser.parse_args()
    
    visualize_profile(args.profile, args.output)


if __name__ == "__main__":
    main()