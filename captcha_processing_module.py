import os
import cv2
import numpy as np

def process_captcha(input_path, contrast, brightness, blur, edge_detection, resize):
    # Read the image
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Resize the image if specified
    if resize != 1.0:
        image = cv2.resize(image, None, fx=resize, fy=resize)

    # Adjust contrast and brightness
    image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

    # Apply blur if specified
    if blur > 0:
        image = cv2.GaussianBlur(image, (2 * blur + 1, 2 * blur + 1), 0)

    # Apply edge detection if specified
    if edge_detection:
        image = cv2.Canny(image, 100, 200)

    # Save the processed image with a unique filename
    output_filename = f"processed_{os.path.basename(input_path)}"
    output_path = os.path.join('processed', output_filename)
    cv2.imwrite(output_path, image)

    return output_filename
