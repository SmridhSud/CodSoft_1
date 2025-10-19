# face_detection_recognition.py
import cv2
import face_recognition
import numpy as np

# Initialize face cascade (for detection) and load known faces (for recognition)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load sample images for recognition (add your own images)
known_image = face_recognition.load_image_file("known_person.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Video capture setup
video_capture = cv2.VideoCapture(0)

while True:
    # Grab frame from webcam
    ret, frame = video_capture.read()
    
    # Face Detection (using Haar Cascades - faster)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Convert to RGB for face_recognition
    rgb_frame = frame[:, :, ::-1]
    
    # Face Recognition for each detected face
    for (x, y, w, h) in faces:
        # Crop face region
        face_image = rgb_frame[y:y+h, x:x+w]
        
        try:
            # Get face encodings
            face_encodings = face_recognition.face_encodings(face_image)
            if len(face_encodings) > 0:
                # Compare with known face
                matches = face_recognition.compare_faces([known_encoding], face_encodings[0])
                face_distances = face_recognition.face_distance([known_encoding], face_encodings[0])
                
                # Best match
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = "Known Person"
                    color = (0, 255, 0)  # Green for recognized
                else:
                    name = "Unknown"
                    color = (0, 0, 255)  # Red for unknown
            else:
                name = "No Face"
                color = (255, 0, 0)  # Blue for detection-only
            
            # Draw rectangle and label
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        except Exception as e:
            print(f"Recognition error: {e}")
            continue
    
    # Display result
    cv2.imshow('Face Detection & Recognition', frame)
    
    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
video_capture.release()
cv2.destroyAllWindows()
