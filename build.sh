#!/bin/bash

# Set the repository name
REPO_NAME="staticsite"
# Construct the base path required for GitHub Pages subdirectories
BASE_PATH="/${REPO_NAME}/"

echo "Building site for production with basepath: ${BASE_PATH}"

# Run the main Python script, passing the calculated base path as a command-line argument
python3 src/main.py "${BASE_PATH}"

echo "Build complete. Site generated in 'docs' directory."