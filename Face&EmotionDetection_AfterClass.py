import cv2
import deepface
from deepface import DeepFace

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        face_roi = frame[y : y + h, x : x + w]

        try:
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            
            if isinstance(result, list):
                emotion = result[0]['dominant_emotion']
            else:
                emotion = result[0]['dominant_emotion']

            cv2.putText(frame, emotion, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
        except Exception as e:
            print("DeepFace error:", e)
            
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f"People Count: {len(faces)}",
                (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    
    cv2.imshow('Face Tracking and Emotion Detection - Press q to Quit', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()