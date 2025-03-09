.PHONY: install test profile clean download-samples stress-test

install:
	pip install -e .

test:
	python -m unittest discover -s tests

profile:
	python -m profiling.profile_processor --input ./data/images --output ./data/output

profile-visualize:
	python -m profiling.run_profiling_with_visualization --input ./data/images --output ./data/output

download-samples:
	python -m scripts.download_sample_images --output ./data/images

stress-test:
	python -m scripts.stress_test --input ./data/images --output ./data/output --iterations 3

clean:
	rm -rf data/output/*
	rm -rf profiling/reports/*
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/utils/__pycache__
	rm -rf tests/__pycache__
	rm -rf profiling/__pycache__
	rm -rf scripts/__pycache__
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist