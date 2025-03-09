# Image Processing Performance Optimization Project

## Project Overview

This project demonstrates how to identify and optimize performance bottlenecks in a Python image processing application using profiling tools and Amazon Q Developer. The application processes images through multiple transformations with intentional inefficiencies that can be optimized.

## Project Structure

```
image-processor/
├── src/                           # Source code directory
│   ├── image_processor.py         # Main application with intentional inefficiencies
│   └── utils/                     # Utility modules
│       └── file_utils.py          # File handling utilities
│
├── scripts/                       # Executable scripts
│   ├── download_sample_images.py  # Script to download sample images
│   ├── run_processor.py           # Main entry point script
│   └── stress_test.py             # Script to run stress tests
│
├── profiling/                     # Profiling tools and results
│   ├── profile_processor.py       # Script to profile the application
│   ├── profile_stress_test.py     # Profiling under stress conditions
│   ├── run_profiling_with_visualization.py  # Visualization runner
│   ├── visualize_profile.py       # Profile visualization utilities
│   └── reports/                   # Directory for profiling data
│
├── data/                          # Data directories
│   ├── images/                    # Directory for input images
│   └── output/                    # Directory for processed images
│
├── tests/                         # Test directory
│   └── test_image_processor.py    # Unit tests for image processor
│
├── setup.py                       # Package installation script
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── project_details.md             # This detailed explanation file
```

## Key Components

### 1. Image Processor (`src/image_processor.py`)

The main application processes images through multiple transformations. It includes several intentional performance issues:

**Inefficient File Listing:**
- The `get_image_files()` method walks through all files multiple times, once for each file extension
- It could be optimized to scan the directory only once

**Unnecessary Image Copies:**
- Each transformation method creates a new copy of the image with `image.copy()`
- This wastes memory and CPU cycles

**Sequential Processing:**
- Images are processed one at a time in a single thread
- Could be optimized with parallel processing using `multiprocessing` or `concurrent.futures`

**Inefficient Algorithms:**
- Uses `Image.NEAREST` for resizing instead of better quality/performance options
- Creates unnecessary intermediate objects

**Memory Inefficiencies:**
- No proper resource management or cleanup
- Excessive copies of image data in memory

**Suboptimal I/O:**
- No error handling for image loading
- Saves images with high quality setting (95) which is inefficient

### 2. Profiler (`profiling/profile_processor.py`)

This script provides three types of profiling:

**CPU Profiling:**
- Uses Python's built-in `cProfile` module
- Identifies which functions consume the most CPU time
- Saves results to a `.prof` file that can be visualized with tools like `snakeviz`

**Memory Profiling:**
- Uses the `memory_profiler` package
- Shows memory consumption over time
- Identifies memory leaks and excessive memory usage

**Time Profiling:**
- Simple timing of the overall execution
- Provides a baseline for measuring optimization improvements

### 3. Sample Image Downloader (`scripts/download_sample_images.py`)

A utility script to download sample images from Unsplash for testing:
- Downloads a specified number of random images
- Configurable image dimensions
- Uses various categories for diverse image content

## Getting Started

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Sample Images:**
   ```bash
   python -m scripts.download_sample_images --count 10
   ```

3. **Run the Image Processor:**
   ```bash
   python -m scripts.run_processor
   ```

4. **Profile the Application:**
   ```bash
   python -m profiling.profile_processor
   ```

5. **Visualize CPU Profile Data:**
   ```bash
   python -m profiling.run_profiling_with_visualization
   ```

## Optimization Opportunities with Amazon Q Developer

After profiling, you can use Amazon Q Developer to help optimize the application in several ways:

### 1. Parallel Processing Implementation

Amazon Q can help implement parallel processing using Python's `multiprocessing` or `concurrent.futures` modules:
- Process multiple images simultaneously
- Utilize all available CPU cores
- Implement a worker pool pattern

### 2. Memory Optimization

Amazon Q can suggest ways to reduce memory usage:
- Eliminate unnecessary image copies
- Implement proper resource cleanup
- Use more memory-efficient data structures and algorithms

### 3. Algorithm Improvements

Amazon Q can recommend more efficient algorithms:
- Better image resizing methods (e.g., `Image.LANCZOS` instead of `Image.NEAREST`)
- More efficient filtering techniques
- Optimized image enhancement approaches

### 4. I/O Optimization

Amazon Q can help improve file handling:
- Implement proper error handling for image loading
- Optimize image saving parameters
- Use more efficient file listing techniques

### 5. Caching Implementation

Amazon Q can suggest caching strategies:
- Cache intermediate results for repeated operations
- Implement memoization for expensive calculations
- Use LRU caching for frequently accessed data

### 6. Code Restructuring

Amazon Q can recommend better code organization:
- Implement a pipeline pattern for image processing
- Use generator expressions for memory efficiency
- Apply design patterns appropriate for image processing workflows

## Demonstration Workflow

1. **Run the Baseline Application:**
   - Process a set of images with the inefficient implementation
   - Record the execution time and resource usage

2. **Profile the Application:**
   - Run the profiling script to identify bottlenecks
   - Analyze the CPU, memory, and time profiling results

3. **Use Amazon Q Developer to Optimize:**
   - Ask Amazon Q to analyze the profiling results
   - Request specific optimizations for identified bottlenecks
   - Implement the suggested improvements

4. **Measure Improvements:**
   - Run the optimized application
   - Compare performance metrics with the baseline
   - Quantify the improvements in execution time and resource usage

5. **Iterate if Needed:**
   - Identify any remaining bottlenecks
   - Apply additional optimizations
   - Measure incremental improvements

This workflow demonstrates how Amazon Q Developer can help organizations identify and resolve performance issues in their applications, leading to more efficient resource utilization and better user experience.