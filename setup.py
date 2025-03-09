#!/usr/bin/env python3
"""
Setup script for the image processor package.
"""

from setuptools import setup, find_packages

setup(
    name="image-processor",
    version="1.0.0",
    description="Efficient image processing with parallel execution capabilities",
    author="Amazon Q Demo",
    author_email="example@example.com",
    packages=find_packages(),
    install_requires=[
        "pillow>=9.0.0",
        "requests>=2.25.0",
        "memory-profiler>=0.60.0",
        "gprof2dot>=2021.2.21",
    ],
    entry_points={
        "console_scripts": [
            "image-processor=scripts.run_processor:main",
            "image-processor-profile=profiling.profile_processor:main",
            "image-processor-stress=scripts.stress_test:main",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)