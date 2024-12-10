import os
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
from captcha_processing_module import process_captcha
from waitress import serve  # Import Waitress

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Ensure an image file is uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Secure the file name
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        return jsonify({"filename": filename, "original_image_url": f"/uploads/{filename}"})


@app.route('/process_captcha', methods=['POST'])
def process_image():
    # Get parameters from the request
    image_name = request.form.get('image_name')
    contrast = float(request.form.get('contrast', 1.0))
    brightness = int(request.form.get('brightness', 0))
    blur = int(request.form.get('blur', 0))
    edge_detection = request.form.get('edge_detection') == 'true'
    resize = float(request.form.get('resize', 1.0))

    input_path = os.path.join(UPLOAD_FOLDER, image_name)

    # Process the image with the provided parameters
    output_image = process_captcha(input_path, contrast, brightness, blur, edge_detection, resize)

    return jsonify({"output_image": output_image})

@app.route('/uploads/<filename>')
def get_uploaded_image(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

@app.route('/processed/<filename>')
def get_processed_image(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename))

if __name__ == '__main__':
    # Run the app using Waitress
    serve(app, host='0.0.0.0', port=5000)
