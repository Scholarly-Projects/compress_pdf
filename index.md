---
title: Home
layout: page
gallery: true
---

<h2>Compress Your PDFs</h2>

<form id="compress-form" action="http://localhost:5000/compress" method="POST" enctype="multipart/form-data">
  <fieldset>
    <legend>Choose Compression Level:</legend>
    <label><input type="radio" name="level" value="light" checked> Light</label>
    <label><input type="radio" name="level" value="medium"> Medium</label>
    <label><input type="radio" name="level" value="strong"> Strong</label>
  </fieldset>

  <br>
  <label for="pdfs">Select PDF(s):</label><br>
  <input type="file" id="pdfs" name="pdfs" accept="application/pdf" multiple required>
  <br><br>

  <input type="submit" value="Compress PDFs">
</form>

<div id="output" style="margin-top: 20px; font-family: monospace;"></div>

<script>
document.getElementById('compress-form').addEventListener('submit', function (e) {
  const output = document.getElementById('output');
  output.innerText = "Uploading and compressing PDFs...";
});
</script>

------

{% include template/credits.html %}

{% include feature/image.html objectid="demo_001" %}
