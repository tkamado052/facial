import cv2
import numpy as np
import base64
import os
from PIL import Image
import io
from flask import Flask, request, jsonify
from flask_cors import CORS  # Add CORS library

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes (less secure, for development only)

dataset_path = 'dataset/'
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# Load Haar cascade classifier for face detection (replace with your path if needed)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        # Extract data from the request body
        data = request.get_json()
        user_id = data['user_id']
        image_data = data['image'].split(',')[1]

        # Decode base64 encoded image data
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        image = np.array(image)

        # Convert image to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces using the cascade classifier
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Generate a unique filename for each captured face
        count = len([name for name in os.listdir(dataset_path) if name.startswith(f"User.{user_id}.")])
        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]

            # Save detected face as JPEG image
            filename = f"{dataset_path}/User.{user_id}.{count}.jpg"
            cv2.imwrite(filename, face_img)

        return jsonify(success=True)

    except Exception as e:
        # Handle exceptions gracefully
        print(f"Error capturing face: {str(e)}")
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    if not os.path.exists('trainer'):
        os.makedirs('trainer')
    app.run(host='127.0.0.1', port=5000, debug=True)  # Specify port and enable debug mode
