# Face Recognition and Attendance Tracking with Flask
This Flask application provides a simple implementation of face recognition for attendance tracking purposes. It allows users to upload images containing faces, recognizes the faces based on preloaded known faces, and logs attendance in a SQLite database.

#Features
- Face Recognition: Recognizes faces in uploaded images against a database of known faces.
- Attendance Tracking: Logs recognized faces along with timestamps into a SQLite database.
- Web Interface: Provides a basic web interface to upload images, view recognized faces, and their attendance records.
- Database Integration: Uses SQLite for storing attendance records.
- Error Handling: Implements basic error handling for file uploads and face recognition failures.
# Setup Instructions
## Prerequisites
- Python 3.x installed on your system.
- Pip package manager installed.
- Git (optional, for cloning the repository).
# Installation
Clone the repository (or download the source code):

```bash
git clone https://github.com/anjaliBaditya/facial-recog
```
# Navigate into the project directory:

Access the application in your web browser:

Open http://localhost:5000 to access the web interface.

Usage
Uploading Images for Face Recognition
Navigate to http://localhost:5000.
Choose an image file containing faces.
Click on the "Upload" button.
The application will recognize faces in the image and update attendance records accordingly.
Viewing Attendance Records
Navigate to http://localhost:5000/view_records.
The page will display a table with attendance records showing recognized faces and timestamps.
Customization
Threshold Adjustment: You can adjust the face recognition threshold (threshold parameter in recognize_face function in app.py) for better accuracy.

Known Faces Database: Add or remove known faces by placing images in the known directory. Ensure images are in .jpg or .png format.

Deployment
For production deployment, consider using a more robust database system like PostgreSQL or MySQL instead of SQLite.
Containerize the application with Docker for easier deployment and scalability.

