# Image Processor Project Details

## Overview

The Image Processor is a Python application designed to efficiently process images through multiple transformations. It supports operations such as resizing, blurring, sharpening, and adjusting contrast and brightness. The application is optimized for performance, with parallel processing capabilities to utilize multi-core processors.

## Project Structure

```
image-processor/
├── src/                           # Source code directory
│   ├── __init__.py                # Make it a proper package
│   ├── image_processor.py         # Core image processing functionality
│   └── utils/                     # Utility modules
│       ├── __init__.py
│       └── file_utils.py          # File handling utilities
│
├── scripts/                       # Executable scripts
│   ├── download_sample_images.py  # Script to download sample images
│   ├── stress_test.py            # Script to run stress tests
│   └── run_processor.py          # Main entry point script
│
├── tests/                         # Test directory
│   ├── __init__.py
│   └── test_image_processor.py   # Unit tests for image processor
│
├── profiling/                     # Profiling tools and results
│   ├── profile_processor.py      # Script to profile the processor
│   ├── profile_stress_test.py    # Script to profile stress tests
│   ├── visualize_profile.py      # Script to visualize profile results
│   ├── run_profiling_with_visualization.py  # Combined profiling script
│   └── reports/                   # Profiling output reports
│
├── docs/                          # Documentation
│   ├── project_details.md        # This file
│   ├── profiling_analysis.md     # Analysis of profiling results
│   └── kcachegrind_usage_guide.md # Guide for using KCachegrind
│
├── data/                          # Data directories
│   ├── images/                    # Input images
│   └── output/                    # Output images
│
├── .gitignore                     # Git ignore file
├── LICENSE                        # License file
├── README.md                      # Project README
├── requirements.txt               # Project dependencies
├── setup.py                       # Package installation script
├── pyproject.toml                 # Modern Python packaging
└── Makefile                       # Common commands
```

## Core Components

### Image Processor (`src/image_processor.py`)

The main class that handles image processing operations. It includes methods for:

- Resizing images
- Applying blur filters
- Sharpening images
- Adjusting contrast and brightness
- Processing images in parallel

### File Utilities (`src/utils/file_utils.py`)

Utility functions for file operations, including:

- Finding image files in a directory
- Ensuring directories exist

### Scripts

- `scripts/run_processor.py`: Main entry point for running the image processor
- `scripts/download_sample_images.py`: Downloads sample images for testing
- `scripts/stress_test.py`: Runs stress tests with multiple images and iterations

### Profiling Tools

- `profiling/profile_processor.py`: Profiles the image processor
- `profiling/profile_stress_test.py`: Profiles the stress test
- `profiling/visualize_profile.py`: Visualizes profiling results
- `profiling/run_profiling_with_visualization.py`: Combined profiling script

## Usage

### Basic Usage

```bash
# Install the package
pip install -e .

# Run the processor
python -m scripts.run_processor --input ./data/images --output ./data/output

# Or using the installed entry point
image-processor --input ./data/images --output ./data/output
```

### Download Sample Images

```bash
python -m scripts.download_sample_images --output ./data/images
# Or using the Makefile
make download-samples
```

### Run Profiling

```bash
python -m profiling.profile_processor --input ./data/images --output ./data/output
# Or using the Makefile
make profile
```

### Run Stress Test

```bash
python -m scripts.stress_test --input ./data/images --output ./data/output --iterations 3
# Or using the Makefile
make stress-test
```

## Performance Optimization

The image processor has been optimized for performance in several ways:

1. **Parallel Processing**: Uses `ProcessPoolExecutor` to process images in parallel
2. **Efficient File Operations**: Optimized file listing with single-pass directory scan
3. **Reduced Memory Usage**: Eliminated unnecessary image copies
4. **Optimized Image Operations**: Better quality/performance balance for resize and save operations
5. **Error Handling**: Proper error handling for file operations and image processing

For detailed performance analysis, see [profiling_analysis.md](profiling_analysis.md).

## Development

### Running Tests

```bash
python -m unittest discover -s tests
# Or using the Makefile
make test
```

### Clean Up

```bash
# Clean up generated files
make clean
```

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.