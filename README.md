# Image Processing Performance Optimization Demo

This project demonstrates how to identify and optimize performance bottlenecks in a Python image processing application using profiling tools and Amazon Q Developer.

## Project Structure

```
image-processor/
├── images/                # Place input images here
├── output/                # Processed images will be saved here
├── profiles/              # Profiling data will be saved here
├── image_processor.py     # Main application with intentional inefficiencies
├── profile_processor.py   # Script to profile the application
├── stress_test.py         # Extended version with more intensive processing
├── profile_stress_test.py # Script to profile the stress test
├── download_sample_images.py  # Script to download sample images
├── profiling_analysis.md  # Analysis of profiling results
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Download sample images using the provided script:

```bash
python download_sample_images.py --count 10
```

## Running the Application

To process images with the inefficient implementation:

```bash
python image_processor.py --input ./images --output ./output
```

## Profiling the Application

To profile the application's performance:

```bash
# Run all profiling types (CPU, memory, time)
python profile_processor.py --input ./images --output ./output

# Run specific profiling type
python profile_processor.py --input ./images --output ./output --profile-type cpu
python profile_processor.py --input ./images --output ./output --profile-type memory
python profile_processor.py --input ./images --output ./output --profile-type time
```

## Stress Testing

For more intensive performance analysis, use the stress test scripts:

### Running the Stress Test

The stress test applies more intensive processing with multiple iterations of each operation:

```bash
# Run with default settings (20 images, 3 iterations per operation)
python stress_test.py

# Customize the stress test
python stress_test.py --iterations 5 --blur-radius 8 --image-count 30
```

Key parameters:
- `--iterations`: Number of times to repeat each operation (default: 3)
- `--blur-radius`: Maximum blur radius to use (default: 5)
- `--image-count`: Target number of images to process (default: 20)

The stress test will automatically duplicate existing images if needed to reach the target count.

### Profiling the Stress Test

```bash
# Run all profiling types on the stress test
python profile_stress_test.py

# Run specific profiling with custom settings
python profile_stress_test.py --profile-type cpu --iterations 4 --image-count 25
```

The stress test profiling results will be saved to `./profiles/stress_profile_stats.prof`.

## Profiling Results

The profiling results are analyzed in detail in the [profiling_analysis.md](./profiling_analysis.md) file. Key findings include:

- Gaussian blur is the most time-consuming operation
- Unnecessary image copies create significant overhead
- Sequential processing doesn't utilize multi-core processors
- Inefficient file listing adds unnecessary overhead

## Visualizing CPU Profile Data

You can visualize the CPU profile data using snakeviz:

```bash
# For regular profiling
snakeviz ./profiles/profile_stats.prof

# For stress test profiling
snakeviz ./profiles/stress_profile_stats.prof
```

## Performance Issues Identified

The application has several performance issues:

1. Inefficient file listing and filtering
2. Unnecessary image copies (25 calls to Image.copy())
3. Sequential processing (no parallelism)
4. Inefficient image loading and saving
5. Suboptimal algorithm choices (e.g., Image.NEAREST for resizing)
6. Redundant image conversions

## Optimization Opportunities

Based on the profiling results, these are the key optimization opportunities:

1. Implement parallel processing with multiprocessing or concurrent.futures
2. Reduce unnecessary image copies
3. Use more efficient algorithms and PIL options
4. Optimize file listing with a single pass approach
5. Add proper error handling
6. Adjust quality settings for better performance

## Recent Changes

- Added stress test scripts for more intensive performance analysis:
  - `stress_test.py`: Extended version with more intensive processing
  - `profile_stress_test.py`: Script to profile the stress test
- Fixed the download_sample_images.py script:
  - Changed `-h` flag to `--ht` to avoid conflict with built-in help
  - Switched image source from Unsplash to Lorem Picsum for more reliable downloads
- Added profiling_analysis.md with detailed performance analysis
- Updated README.md with more comprehensive information