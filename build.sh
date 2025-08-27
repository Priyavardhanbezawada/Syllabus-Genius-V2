#!/usr/bin/env bash
# exit on error
set -o errexit

# Run the package manager with superuser privileges and auto-confirm all prompts.
# This is a more robust way to install system dependencies on services like Render.
sudo apt-get update -y
sudo apt-get install -y tesseract-ocr

# Install Python dependencies after system packages are ready
pip install -r requirements.txt
