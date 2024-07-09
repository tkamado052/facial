from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import mysql.connector
import base64

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
cursor = db.cursor()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')  # Assuming trainer.yml is present in trainer directory

@app.route('/')
def index():
    username = request.args.get('username', 'Guest')
    return render_template('index.html', username=username)

@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image uploaded'}), 400

    image = data['image'].split(',')[1]  # Base64 part after the comma
    image_array = np.frombuffer(base64.b64decode(image), dtype=np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return jsonify({'message': 'No face detected in image'}), 404

    for (x, y, w, h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        if confidence < 100:
            cursor.execute("SELECT username FROM test3 WHERE id = %s", (id,))
            user = cursor.fetchone()
            name = user[0] if user else "Unknown"
            confidence = f"  {round(100 - confidence)}%"
            return jsonify({'name': name, 'confidence': confidence})
        else:
            return jsonify({'name': 'Unknown', 'confidence': f"  {round(100 - confidence)}%"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
