# Image Processing Performance Optimization Demo

This project demonstrates how to identify and optimize performance bottlenecks in a Python image processing application using profiling tools and Amazon Q Developer.

## Project Structure

```
image-processor/
├── images/           # Place input images here
├── output/           # Processed images will be saved here
├── profiles/         # Profiling data will be saved here
├── image_processor.py  # Main application with intentional inefficiencies
├── profile_processor.py  # Script to profile the application
├── download_sample_images.py  # Script to download sample images
├── profiling_analysis.md  # Analysis of profiling results
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Download sample images using the provided script:

```bash
python download_sample_images.py --count 5
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

## Profiling Results

The profiling results are analyzed in detail in the [profiling_analysis.md](./profiling_analysis.md) file. Key findings include:

- Gaussian blur is the most time-consuming operation
- Unnecessary image copies create significant overhead
- Sequential processing doesn't utilize multi-core processors
- Inefficient file listing adds unnecessary overhead

## Visualizing CPU Profile Data

You can visualize the CPU profile data using snakeviz:

```bash
snakeviz ./profiles/profile_stats.prof
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

- Fixed the download_sample_images.py script:
  - Changed `-h` flag to `--ht` to avoid conflict with built-in help
  - Switched image source from Unsplash to Lorem Picsum for more reliable downloads
- Added profiling_analysis.md with detailed performance analysis
- Updated README.md with more comprehensive information