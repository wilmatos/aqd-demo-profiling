# Image Processor

A high-performance image processing application with parallel execution capabilities.

## Features

- Process multiple images in parallel using multi-core processing
- Apply various transformations to images:
  - Resize
  - Blur
  - Sharpen
  - Adjust contrast
  - Adjust brightness
- Optimized for performance and memory efficiency
- Comprehensive profiling and testing tools

## Installation

### Prerequisites

- Python 3.6 or higher
- pip

### Install from source

```bash
# Clone the repository
git clone https://github.com/yourusername/image-processor.git
cd image-processor

# Install the package in development mode
pip install -e .
```

### Install dependencies only

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Process images using the command-line interface
image-processor --input ./data/images --output ./data/output

# Or run the script directly
python -m scripts.run_processor --input ./data/images --output ./data/output
```

### Download Sample Images

```bash
# Download sample images for testing
python -m scripts.download_sample_images --output ./data/images

# Or use the Makefile
make download-samples
```

### Run Profiling

```bash
# Profile the image processor
python -m profiling.profile_processor --input ./data/images --output ./data/output

# Or use the Makefile
make profile

# Generate visualization of profiling results
python -m profiling.run_profiling_with_visualization
# Or use the Makefile
make profile-visualize
```

### Run Stress Test

```bash
# Run a stress test with multiple iterations
python -m scripts.stress_test --input ./data/images --output ./data/output --iterations 3

# Or use the Makefile
make stress-test
```

## Repository Structure

```
image-processor/
├── src/                           # Source code directory
│   ├── image_processor.py         # Core image processing functionality
│   ├── __init__.py               # Package initialization
│   └── utils/                     # Utility modules
│       └── file_utils.py         # File handling utilities
│
├── scripts/                       # Executable scripts
│   ├── download_sample_images.py  # Script to download sample images
│   ├── stress_test.py            # Script to run stress tests
│   └── run_processor.py          # Main entry point script
│
├── tests/                         # Test directory
│   ├── __init__.py               # Test package initialization
│   └── test_image_processor.py   # Unit tests for image processor
│
├── profiling/                     # Profiling tools and results
│   ├── profile_processor.py       # CPU and memory profiling
│   ├── profile_stress_test.py    # Profiling under stress conditions
│   ├── run_profiling_with_visualization.py  # Visualization of profiling results
│   ├── visualize_profile.py      # Profile visualization utilities
│   ├── reports/                  # Directory for profiling reports
│   └── __init__.py              # Profiling package initialization
│
├── data/                         # Data directories
│   ├── images/                   # Input images directory
│   └── output/                   # Processed images output directory
│
├── docs/                         # Documentation files
│   ├── project_details.md        # Detailed project information
│   ├── profiling_analysis.md     # Analysis of profiling results
│   └── kcachegrind_usage_guide.md # Guide for KCachegrind usage
│
├── .github/                      # GitHub specific files
│   └── workflows/                # GitHub Actions workflows
│
├── setup.py                      # Package setup file
├── requirements.txt              # Project dependencies
├── LICENSE                       # MIT License file
├── README.md                     # Project documentation
├── .gitignore                   # Git ignore rules
└── devfile.yaml                 # Development environment configuration
```

## Data Flow

```mermaid
graph TD
    A[Input Images] --> B[Image Processor]
    B --> C{Parallel Processing}
    C --> |Worker 1| D[Image Pipeline]
    C --> |Worker 2| E[Image Pipeline]
    C --> |Worker N| F[Image Pipeline]
    
    subgraph "Image Pipeline"
        D --> D1[Resize]
        D1 --> D2[Blur]
        D2 --> D3[Sharpen]
        D3 --> D4[Contrast]
        D4 --> D5[Brightness]
    end
    
    D5 --> G[Processed Images]
    E --> G
    F --> G
    
    H[Profile Monitor] -.-> B
    H -.-> C
    H -.-> D
    
    I[Stress Test] --> |Input| B
    I --> |Metrics| J[Performance Reports]
```

## Documentation

- [Project Details](project_details.md) - Detailed information about the project structure and components
- [Profiling Analysis](profiling_analysis.md) - Analysis of performance profiling results
- [KCachegrind Usage Guide](kcachegrind_usage_guide.md) - Guide for using KCachegrind with profiling results

## Development

### Running Tests

```bash
# Run unit tests
python -m unittest discover -s tests

# Or use the Makefile
make test
```

### Clean Up

```bash
# Clean up generated files
make clean
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.