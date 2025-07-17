# PDF Compression Tool Setup Guide (macOS)

This guide will help you set up the PDF compression tool on your macOS system using Python virtual environments.

## Prerequisites
- macOS 10.15 (Catalina) or newer
- Xcode Command Line Tools
- Homebrew package manager

## Step 1: 

python3.11 -m venv .venv

source .venv/bin/activate

pip install python-dotenv

pip install -U pip wheel

pip install flask flask-cors pymupdf pillow pikepdf

# Terminal 1: Jekyll frontend
jekyll s --baseurl /compress_pdf

# Terminal 2: Flask backend
source .venv/bin/activate
flask run