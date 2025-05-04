#!/bin/bash

echo "Running static site generator..."
python3 src/main.py

echo "Starting development server on http://localhost:8888..."
# Change directory to public and start the server
# Use exec to replace the shell process with the server process,
# so Ctrl+C stops the server directly. Or just run it normally.
cd public && python3 -m http.server 8888