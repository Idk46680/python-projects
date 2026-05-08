import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

def count_fingers(contour):
    hull = cv2.convexHull(contour, returnPoints=False)
    
    if hull is None or len(hull) < 3:
        return 0
    
    defects = cv2.convexityDefects(contour, hull)

    if defects is None:
        return 0
    
    finger_count = 0

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i][0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])

        a = np.linalg.norm(np.array(end) - np.array(start))
        b = np.linalg.norm(np.array(far) - np.array(start))
        c = np.linalg.norm(np.array(end) - np.array(far))

        angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c + 1e-5))

        if angle <= np.pi / 2:
            finger_count += 1

    return finger_count


while True:
    ret, frame = cap.read()

    if not ret: 
        print("Error: Failed to capture image.")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0, 20, 70], dtype = np.uint8)
    upper_skin = np.array([20, 255, 255], dtype = np.uint8)

    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 500:

            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            center_x = int(x + w / 2)
            center_y = int(y + h / 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            hull_points = cv2.convexHull(max_contour)
            cv2.drawContours(frame, [hull_points], -1, (255, 0, 0), 2)

            fingers = count_fingers(max_contour)

            if fingers == 0:
                gesture = "Fist"
            elif fingers == 1:
                gesture = "Thumbs Up (maybe)"
            elif fingers >= 4:
                gesture = "Open Hand"
            else:
                gesture = "Unknown"

            cv2.putText(frame, gesture, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 255), 2)

    cv2.imshow('Original Frame', frame)
    cv2.imshow('Filtered Frame', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 