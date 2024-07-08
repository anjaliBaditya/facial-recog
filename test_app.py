from flask import Flask, request, jsonify, render_template
import face_recognition
import os
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Path to directory containing known faces images
known_faces_dir = "known"

# Initialize SQLite database for attendance records
db_path = 'attendance.db'

def initialize_database():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Create tables if they do not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def load_known_faces(directory):
    known_faces = []
    known_names = []

    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join(directory, filename)
            image = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(os.path.splitext(filename)[0])

    return known_faces, known_names

def recognize_face(unknown_image, known_faces, known_names, threshold=0.6):
    unknown_encoding = face_recognition.face_encodings(unknown_image)

    if len(unknown_encoding) > 0:
        face_distances = face_recognition.face_distance(known_faces, unknown_encoding[0])
        min_distance_index = face_distances.argmin()

        if face_distances[min_distance_index] < threshold:
            return known_names[min_distance_index]
        else:
            return "Unknown"
    else:
        return "No face found in the provided image"

# Initialize database on startup
initialize_database()

# Load known faces and names
known_faces, known_names = load_known_faces(known_faces_dir)

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        unknown_image = face_recognition.load_image_file(file)
        result = recognize_face(unknown_image, known_faces, known_names)

        # Update attendance records in database
        if result != "Unknown":
            update_attendance_db(result)

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_attendance_db(name):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO attendance (name) VALUES (?)
        ''', (name,))
        conn.commit()

@app.route('/view_records', methods=['GET'])
def view_records():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, timestamp FROM attendance ORDER BY timestamp DESC
        ''')
        records = cursor.fetchall()
        return render_template('attendance_records.html', records=records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
