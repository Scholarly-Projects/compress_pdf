# PDF Compression Tool Setup Guide (macOS)

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
