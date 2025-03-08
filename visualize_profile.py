#!/usr/bin/env python3
"""
Script to convert Python profiling data to KCachegrind format and open it.
"""

import os
import sys
import argparse
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_and_open(profile_file, output_file=None, open_viewer=True):
    """
    Convert a Python profile file to KCachegrind format and optionally open it.
    
    Args:
        profile_file: Path to the Python profile file (.prof)
        output_file: Path to save the KCachegrind file (.calltree)
        open_viewer: Whether to open KCachegrind after conversion
    """
    if not os.path.exists(profile_file):
        logger.error(f"Profile file not found: {profile_file}")
        return False
    
    # If no output file specified, create one with .calltree extension
    if output_file is None:
        base, _ = os.path.splitext(profile_file)
        output_file = f"{base}.calltree"
    
    # Convert the profile file to KCachegrind format
    try:
        logger.info(f"Converting {profile_file} to KCachegrind format...")
        subprocess.run(
            ["pyprof2calltree", "-i", profile_file, "-o", output_file],
            check=True
        )
        logger.info(f"Conversion successful. Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting profile: {e}")
        return False
    except FileNotFoundError:
        logger.error("pyprof2calltree not found. Please install it with: pip install pyprof2calltree")
        return False
    
    # Open KCachegrind if requested
    if open_viewer:
        try:
            logger.info("Opening KCachegrind...")
            subprocess.Popen(["kcachegrind", output_file])
            logger.info("KCachegrind opened successfully")
        except FileNotFoundError:
            logger.error("KCachegrind not found. Please install it with: sudo apt-get install kcachegrind")
            return False
        except Exception as e:
            logger.error(f"Error opening KCachegrind: {e}")
            return False
    
    return True

def main():
    """Parse command line arguments and run the converter."""
    parser = argparse.ArgumentParser(
        description='Convert Python profiling data to KCachegrind format and open it.'
    )
    parser.add_argument('profile_file', help='Path to the Python profile file (.prof)')
    parser.add_argument('--output', '-o', help='Output file path (.calltree)')
    parser.add_argument('--no-open', '-n', action='store_true',
                        help='Do not open KCachegrind after conversion')
    
    args = parser.parse_args()
    
    convert_and_open(
        args.profile_file,
        args.output,
        not args.no_open
    )

if __name__ == "__main__":
    main()