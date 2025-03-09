#!/usr/bin/env python3
"""
Performance comparison script for image processing implementations.

This script compares the performance of the original image processor
with the optimized implementation.
"""

import os
import time
import argparse
import logging
import multiprocessing
from image_processor import ImageProcessor as OriginalImageProcessor
from optimized_image_processor import ImageProcessor as OptimizedImageProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_test(processor_class, input_dir, output_dir, name="Unnamed"):
    """Run a processing test with the given processor class and measure performance."""
    # Create output directory with test name
    test_output_dir = os.path.join(output_dir, name.lower().replace(" ", "_"))
    if not os.path.exists(test_output_dir):
        os.makedirs(test_output_dir)
    
    # Initialize processor
    processor = processor_class(input_dir, test_output_dir)
    
    # Record start time and memory
    start_time = time.time()
    
    # Process all images
    processor.process_all_images()
    
    # Record end time
    end_time = time.time()
    elapsed = end_time - start_time
    
    logger.info(f"{name} processing completed in {elapsed:.2f} seconds")
    return elapsed

def compare_performance(input_dir, output_dir, repeat=3):
    """Compare performance between original and optimized implementations."""
    results = {
        "Original": [],
        "Optimized": []
    }
    
    logger.info(f"Starting performance comparison with {repeat} repetitions...")
    
    for i in range(repeat):
        logger.info(f"Running test iteration {i+1}/{repeat}")
        
        # Run original processor
        orig_time = run_test(
            OriginalImageProcessor, 
            input_dir, 
            os.path.join(output_dir, f"run_{i+1}"),
            "Original"
        )
        results["Original"].append(orig_time)
        
        # Run optimized processor
        opt_time = run_test(
            OptimizedImageProcessor, 
            input_dir, 
            os.path.join(output_dir, f"run_{i+1}"),
            "Optimized"
        )
        results["Optimized"].append(opt_time)
        
        # Calculate improvement
        improvement = (orig_time - opt_time) / orig_time * 100
        logger.info(f"Iteration {i+1} speedup: {improvement:.2f}%")
    
    # Calculate average results
    avg_original = sum(results["Original"]) / len(results["Original"])
    avg_optimized = sum(results["Optimized"]) / len(results["Optimized"])
    avg_improvement = (avg_original - avg_optimized) / avg_original * 100
    
    # Calculate theoretical max parallel speedup
    cpu_count = multiprocessing.cpu_count()
    theoretical_max = min(cpu_count, 100)  # Assuming we don't get more than 100x speedup
    
    logger.info("\n===== PERFORMANCE COMPARISON RESULTS =====")
    logger.info(f"Average original processing time: {avg_original:.2f} seconds")
    logger.info(f"Average optimized processing time: {avg_optimized:.2f} seconds")
    logger.info(f"Average speedup: {avg_improvement:.2f}%")
    logger.info(f"Speedup factor: {avg_original/avg_optimized:.2f}x")
    logger.info(f"Number of CPU cores: {cpu_count}")
    logger.info(f"Efficiency (% of theoretical max parallel speedup): {100 * (avg_original/avg_optimized) / theoretical_max:.2f}%")
    
    return {
        "original_time": avg_original,
        "optimized_time": avg_optimized,
        "improvement_percent": avg_improvement,
        "speedup_factor": avg_original/avg_optimized,
        "cpu_count": cpu_count,
        "efficiency": (avg_original/avg_optimized) / theoretical_max
    }

def main():
    """Parse arguments and run the comparison."""
    parser = argparse.ArgumentParser(description='Compare original vs optimized image processing performance')
    parser.add_argument('--input', '-i', default='./images', help='Directory containing input images')
    parser.add_argument('--output', '-o', default='./comparison_output', help='Base directory for output')
    parser.add_argument('--repeat', '-r', type=int, default=3, help='Number of test repetitions')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Run comparison
    compare_performance(args.input, args.output, args.repeat)

if __name__ == "__main__":
    main()