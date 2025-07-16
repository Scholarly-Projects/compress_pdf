# compressor.py
import platform, subprocess, io, tempfile
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import pikepdf

compression_settings = {
    'light':  dict(suffix='_lcom.pdf', dpi=300, quality=80),
    'medium': dict(suffix='_mcom.pdf', dpi=144, quality=65),
    'strong': dict(suffix='_scom.pdf', dpi=72,  quality=50),
}

def remove_quarantine_mac(path: Path):
    if platform.system() == 'Darwin':
        try:
            subprocess.run(['xattr', '-d', 'com.apple.quarantine', str(path)])
        except Exception:
            pass

def compress_pdf(input_path: Path, output_path: Path, dpi: int, quality: int):
    doc = fitz.open(str(input_path))
    for page in doc:
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            img_dict = doc.extract_image(xref)
            orig_data = img_dict['image']
            img = Image.open(io.BytesIO(orig_data))

            src_dpi = img.info.get('dpi', (300, 300))[0]
            scale = dpi / src_dpi
            new_size = (int(img.width * scale), int(img.height * scale))
            if new_size[0] > 0 and new_size[1] > 0:
                img = img.resize(new_size, Image.LANCZOS)

            buf = io.BytesIO()
            img.convert('RGB').save(buf, format='JPEG', quality=quality)
            new_data = buf.getvalue()

            if len(new_data) < len(orig_data):
                doc.update_stream(xref, new_data)

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmpf:
        tmp_path = Path(tmpf.name)
    try:
        doc.save(tmp_path, garbage=4, deflate=True)
    finally:
        doc.close()

    with pikepdf.open(tmp_path) as pdf:
        pdf.save(str(output_path), linearize=True, compress_streams=True)
    tmp_path.unlink()

    remove_quarantine_mac(output_path)
    return output_path.name
