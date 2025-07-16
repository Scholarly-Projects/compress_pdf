from flask import Flask, request, send_file
from flask_cors import CORS
import io, zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile
from compress import compress_pdf, compression_settings  # your compressor logic

app = Flask(__name__)
# Allow requests from your GitHub Pages frontend domain (adjust as needed)
CORS(app, origins=["https://aweymo-ui.github.io"])

@app.route('/compress', methods=['POST'])
def compress_pdfs():
    level = request.form.get('level', 'medium')
    settings = compression_settings.get(level)
    if not settings:
        return "Invalid compression level", 400

    uploaded_files = request.files.getlist('pdfs')
    if not uploaded_files:
        return "No PDFs uploaded.", 400

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in uploaded_files:
            with NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
                input_tmp.write(file.read())
                input_path = Path(input_tmp.name)

            output_path = input_path.parent / f"{input_path.stem}_compressed.pdf"

            try:
                compress_pdf(
                    input_path=input_path,
                    output_path=output_path,
                    dpi=settings['dpi'],
                    quality=settings['quality']
                )
                with open(output_path, 'rb') as f:
                    zipf.writestr(output_path.name, f.read())
            finally:
                input_path.unlink(missing_ok=True)
                output_path.unlink(missing_ok=True)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='compressed_pdfs.zip'
    )

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
