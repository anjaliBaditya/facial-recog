import cv2
import requests
import json

# Set the API endpoint
api_url = "http://172.31.141.86:5000/recognize"

# Load the pre-trained face detection model from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Capture the face image
        face_image = frame[y:y+h, x:x+w]

        # Save the captured face image
        cv2.imwrite("captured_face.jpg", face_image)

        # Send the captured image to the API for recognition
        files = {'image': open('captured_face.jpg', 'rb')}
        response = requests.post(api_url, files=files)

        # Parse the API response
        try:
            result = response.json()
            name = result.get('name', 'Unknown')
            print(f"Recognized person: {name}")
        except json.JSONDecodeError:
            print("Error decoding API response")

    # Display the frame
    cv2.imshow('Face Recognition', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
