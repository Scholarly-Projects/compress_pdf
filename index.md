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
const isGitHubPages = window.location.hostname === 'scholarly-projects.github.io';

let BACKEND_URL;
if (isLocal) {
    BACKEND_URL = 'http://localhost:5000/compress';
} else if (isGitHubPages) {
    BACKEND_URL = 'https://compress-pdf.herokuapp.com/compress';
} else {
    BACKEND_URL = 'https://compress-pdf.herokuapp.com/compress';
}

document.getElementById('compress-form').addEventListener('submit', async (e) => {
  // ... rest of your code ...
});
</script>

------

{% include template/credits.html %}

{% include feature/image.html objectid="demo_001" %}