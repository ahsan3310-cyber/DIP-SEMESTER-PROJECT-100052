const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const fileNameDisplay = document.getElementById('file-name');
const processSection = document.getElementById('process-section');
const denoiseBtn = document.getElementById('denoise-btn');
const loadingSpinner = document.getElementById('loading-spinner');
const resultSection = document.getElementById('result-section');
const originalImage = document.getElementById('original-image');
const processedImage = document.getElementById('processed-image');
const downloadLink = document.getElementById('download-link');

let selectedFile = null;

// Drag & Drop
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => uploadArea.classList.add('dragover'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('dragover'), false);
});

uploadArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

function handleFiles(files) {
    if (files.length > 0) {
        selectedFile = files[0];
        if (!selectedFile.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }
        fileNameDisplay.textContent = `Selected: ${selectedFile.name}`;
        
        // Preview Original
        const reader = new FileReader();
        reader.onload = (e) => {
            originalImage.src = e.target.result;
            processSection.style.display = 'block';
            resultSection.style.display = 'none'; // Hide previous results if any
        };
        reader.readAsDataURL(selectedFile);
    }
}

// Button Click
denoiseBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    // Loading State
    denoiseBtn.disabled = true;
    loadingSpinner.style.display = 'block';
    denoiseBtn.querySelector('span').textContent = 'Processing...';

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/api/denoise', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Processing failed');
        }

        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);

        processedImage.src = imageUrl;
        downloadLink.href = imageUrl;
        
        resultSection.style.display = 'block';
        processSection.style.display = 'none'; // Hide process button after success
        uploadArea.style.display = 'none'; // Hide upload area for cleaner look

    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    } finally {
        // Reset Button State
        denoiseBtn.disabled = false;
        loadingSpinner.style.display = 'none';
        denoiseBtn.querySelector('span').textContent = 'Clean Image';
    }
});
