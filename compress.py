import io
import os
import platform
import subprocess
import tempfile
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import pikepdf

compression_settings = {
    'light':  {'suffix': '_lcom.pdf', 'dpi': 300, 'quality': 80},
    'medium': {'suffix': '_mcom.pdf', 'dpi': 144, 'quality': 65},
    'strong': {'suffix': '_scom.pdf', 'dpi': 72,  'quality': 50},
}

def remove_quarantine_flag(path: Path):
    """Remove macOS quarantine attribute silently"""
    if platform.system() == 'Darwin':
        try:
            subprocess.run(['xattr', '-d', 'com.apple.quarantine', str(path)], 
                          stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=False)
        except Exception:
            pass

def compress_pdf(input_path: Path, output_path: Path, dpi: int, quality: int):
    """Optimized PDF compression with error handling"""
    try:
        with fitz.open(input_path) as doc:
            for page in doc:
                for img_info in page.get_images(full=True):
                    xref = img_info[0]
                    base_img = doc.extract_image(xref)
                    img_bytes = base_img["image"]
                    
                    try:
                        with Image.open(io.BytesIO(img_bytes)) as img:
                            # Handle missing/invalid DPI metadata
                            src_dpi = img.info.get('dpi', (300, 300))[0] or 300
                            scale = dpi / src_dpi
                            
                            if scale < 1.0:  # Only downscale
                                new_size = (int(img.width * scale), int(img.height * scale))
                                img = img.resize(new_size, Image.LANCZOS)
                            
                            buf = io.BytesIO()
                            img.convert('RGB').save(buf, format='JPEG', quality=quality)
                            new_data = buf.getvalue()
                            
                            if len(new_data) < len(img_bytes):
                                doc.update_stream(xref, new_data)
                    except (IOError, Image.DecompressionBombError):
                        continue  # Skip problematic images
            
            # Save optimized document
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_path = Path(tmp_file.name)
                doc.save(tmp_path, garbage=4, deflate=True)
            
            # Further optimize with pikepdf
            with pikepdf.open(tmp_path) as pdf:
                pdf.save(output_path, linearize=True, compress_streams=True)
            os.unlink(tmp_path)
            
        remove_quarantine_flag(output_path)
        return True
    except Exception as e:
        print(f"Compression error: {str(e)}")
        return False
    