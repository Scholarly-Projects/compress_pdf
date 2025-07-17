import os
import io
import zipfile
import tempfile
from pathlib import Path
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from compress import compress_pdf, compression_settings

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:4000,http://127.0.0.1:4000,https://scholarly-projects.github.io').split(',')
CORS(app, origins=cors_origins)

# Configuration from environment variables
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE_MB', 50)) * 1024 * 1024  # 50MB default
MAX_TOTAL_SIZE = int(os.getenv('MAX_TOTAL_SIZE_MB', 200)) * 1024 * 1024  # 200MB default
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/compress', methods=['POST'])
def handle_compression():
    # Validate compression level
    level = request.form.get('level', 'medium')
    if level not in compression_settings:
        return jsonify({"error": "Invalid compression level"}), 400
    
    settings = compression_settings[level]
    
    # Validate files
    if 'pdfs' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
        
    files = request.files.getlist('pdfs')
    if not files or files[0].filename == '':
        return jsonify({"error": "No selected files"}), 400
    
    # Validate file sizes
    total_size = 0
    for file in files:
        if not allowed_file(file.filename):
            return jsonify({"error": f"Invalid file type: {file.filename}"}), 400
        
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({"error": f"File too large: {file.filename} ({file_size//1024}KB)"}), 400
        
        total_size += file_size
        if total_size > MAX_TOTAL_SIZE:
            return jsonify({"error": "Total upload size exceeds limit"}), 400

    # Process files
    zip_buffer = io.BytesIO()
    processed_files = []
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            try:
                filename = secure_filename(file.filename)
                stem = Path(filename).stem
                output_name = f"{stem}{settings['suffix']}"
                
                # Create temporary files
                with tempfile.NamedTemporaryFile(suffix='.pdf') as input_tmp:
                    # Save uploaded file to temp
                    file.save(input_tmp.name)
                    input_path = Path(input_tmp.name)
                    
                    # Create output path
                    output_path = Path(f"{stem}_compressed.pdf")
                    
                    # Compress the file
                    if compress_pdf(input_path, output_path, settings['dpi'], settings['quality']):
                        # Add to zip
                        zipf.write(output_path, output_name)
                        processed_files.append(output_name)
                    
                    # Clean up output file
                    if output_path.exists():
                        output_path.unlink()
            except Exception as e:
                print(f"Error processing {file.filename}: {str(e)}")
    
    if not processed_files:
        return jsonify({"error": "No files processed successfully"}), 500
    
    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='compressed_pdfs.zip'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)