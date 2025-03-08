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
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Place some sample images in the `images/` directory.

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

## Visualizing CPU Profile Data

You can visualize the CPU profile data using snakeviz:

```bash
snakeviz ./profiles/profile_stats.prof
```

## Performance Issues to Identify

The application has several intentional performance issues:

1. Inefficient file listing and filtering
2. Unnecessary image copies
3. Sequential processing (no parallelism)
4. Inefficient image loading and saving
5. Suboptimal algorithm choices
6. Memory inefficiencies

## Optimization Opportunities

After profiling, you can use Amazon Q Developer to help optimize:

1. Implement parallel processing with multiprocessing or concurrent.futures
2. Reduce unnecessary image copies
3. Use more efficient algorithms and PIL options
4. Implement caching where appropriate
5. Optimize memory usage
6. Improve file handling efficiency