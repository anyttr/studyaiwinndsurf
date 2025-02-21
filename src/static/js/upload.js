document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const uploadStatus = document.getElementById('upload-status');

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const file = fileInput.files[0];
        if (!file) {
            showError('Please select a file');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await uploadFile(formData);
            if (response.ok) {
                const result = await response.json();
                showSuccess('File uploaded successfully!');
                displayProcessingResult(result);
            } else {
                const error = await response.json();
                showError(error.error || 'Upload failed');
            }
        } catch (error) {
            showError('Network error occurred');
        }
    });

    async function uploadFile(formData) {
        const xhr = new XMLHttpRequest();
        
        // Setup progress tracking
        xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                updateProgress(percentComplete);
            }
        });

        return await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
    }

    function updateProgress(percent) {
        progressBar.style.width = percent + '%';
        progressText.textContent = Math.round(percent) + '%';
    }

    function showError(message) {
        uploadStatus.className = 'error';
        uploadStatus.textContent = message;
    }

    function showSuccess(message) {
        uploadStatus.className = 'success';
        uploadStatus.textContent = message;
    }

    function displayProcessingResult(result) {
        // Create a section to display processing results
        const resultDiv = document.createElement('div');
        resultDiv.className = 'processing-result';
        
        // Display different information based on file type
        switch(result.type) {
            case 'text':
                resultDiv.innerHTML = `
                    <h3>Text Processing Result</h3>
                    <p>Content Length: ${result.length} characters</p>
                    <div class="content-preview">${result.content}</div>
                `;
                break;
            case 'image':
                resultDiv.innerHTML = `
                    <h3>Image Processing Result</h3>
                    <p>Dimensions: ${result.dimensions[0]}x${result.dimensions[1]}</p>
                    <div class="extracted-text">${result.text_content}</div>
                `;
                break;
            case 'audio':
                resultDiv.innerHTML = `
                    <h3>Audio Processing Result</h3>
                    <div class="transcription">${result.transcription || result.error}</div>
                `;
                break;
            case 'video':
                resultDiv.innerHTML = `
                    <h3>Video Processing Result</h3>
                    <div class="status">${result.status}</div>
                `;
                break;
        }

        // Add the result to the page
        const resultsContainer = document.getElementById('processing-results');
        resultsContainer.insertBefore(resultDiv, resultsContainer.firstChild);
    }
});
