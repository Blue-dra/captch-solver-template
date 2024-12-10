let uploadedImageUrl = "";
let uploadedImageName = "";

document.getElementById('uploadButton').addEventListener('click', function() {
    let fileInput = document.getElementById('fileInput');
    let formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        uploadedImageUrl = data.original_image_url;
        uploadedImageName = data.filename;
        
        // Display the uploaded image
        document.getElementById('uploadedImage').style.display = 'block';
        document.getElementById('uploadedImage').src = uploadedImageUrl;

        // Show control components and the "Show Processed Image" button
        document.getElementById('controls').style.display = 'block';
        document.getElementById('showButton').style.display = 'block';
    })
    .catch(error => console.error('Error uploading image:', error));
});

document.getElementById('showButton').addEventListener('click', function() {
    let contrast = document.getElementById('contrast').value;
    let brightness = document.getElementById('brightness').value;
    let blur = document.getElementById('blur').value;
    let edgeDetection = document.getElementById('edgeDetection').checked;
    let resize = document.getElementById('resize').value;

    let formData = new FormData();
    formData.append('image_name', uploadedImageName);  // Pass the filename
    formData.append('contrast', contrast);
    formData.append('brightness', brightness);
    formData.append('blur', blur);
    formData.append('edge_detection', edgeDetection);
    formData.append('resize', resize);

    fetch('/process_captcha', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let processedImage = document.getElementById('processedImage');
        processedImage.style.display = 'block';
        processedImage.src = '/processed/' + data.output_image;
    })
    .catch(error => console.error('Error processing image:', error));
});
