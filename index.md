---
title: PDF Compressor
layout: page
---

<div class="container py-5">
  <h2 class="text-center mb-4">PDF Compression Tool</h2>
  
  <div class="card shadow-sm">
    <div class="card-body">
      <form id="compress-form" enctype="multipart/form-data">
        <div class="mb-3">
          <label class="form-label">Compression Level:</label>
          <div class="btn-group w-100" role="group">
            <input type="radio" class="btn-check" name="level" id="light" value="light" autocomplete="off" checked>
            <label class="btn btn-outline-primary" for="light">Light</label>
            
            <input type="radio" class="btn-check" name="level" id="medium" value="medium" autocomplete="off">
            <label class="btn btn-outline-primary" for="medium">Medium</label>
            
            <input type="radio" class="btn-check" name="level" id="strong" value="strong" autocomplete="off">
            <label class="btn btn-outline-primary" for="strong">Strong</label>
          </div>
        </div>
        
        <div class="mb-3">
          <label for="pdf-upload" class="form-label">Select PDF Files:</label>
          <input class="form-control" type="file" id="pdf-upload" accept=".pdf" multiple required>
        </div>
        
        <button type="submit" class="btn btn-primary w-100">
          <span id="submit-text">Compress PDFs</span>
          <div id="spinner" class="spinner-border spinner-border-sm d-none" role="status"></div>
        </button>
      </form>
      
      <div id="result" class="mt-4"></div>
    </div>
  </div>
</div>

<script>
// Determine backend URL based on environment
const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const BACKEND_URL = isLocal 
    ? 'http://localhost:5000/compress' 
    : 'https://your-actual-backend-url.com/compress'; 

document.getElementById('compress-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const files = document.getElementById('pdf-upload').files;
  const level = document.querySelector('input[name="level"]:checked').value;
  const spinner = document.getElementById('spinner');
  const submitText = document.getElementById('submit-text');
  const resultDiv = document.getElementById('result');
  
  // UI updates
  spinner.classList.remove('d-none');
  submitText.textContent = 'Processing...';
  resultDiv.innerHTML = '<div class="alert alert-info">Compressing files...</div>';
  
  try {
    const formData = new FormData();
    formData.append('level', level);
    for (let i = 0; i < files.length; i++) {
      formData.append('pdfs', files[i]);
    }
    
    const response = await fetch(BACKEND_URL, {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'compressed_pdfs.zip';
      document.body.appendChild(a);
      a.click();
      a.remove();
      resultDiv.innerHTML = '<div class="alert alert-success">Download started!</div>';
    } else {
      const error = await response.json();
      resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.error}</div>`;
    }
  } catch (error) {
    resultDiv.innerHTML = `<div class="alert alert-danger">Network error: ${error.message}</div>`;
  } finally {
    spinner.classList.add('d-none');
    submitText.textContent = 'Compress PDFs';
  }
});
</script>

------

{% include template/credits.html %}

{% include feature/image.html objectid="demo_001" %}