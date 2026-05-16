import cv2, time, pyautogui
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75, min_tracking_confidence=0.75)
mp_drawing = mp.solutions.drawing_utils

BASE_SCROLL_SPEED = 150
SCROLL_DELAY = 0.25
CAM_WIDTH, CAM_HEIGHT = 640, 480

paused = False
last_action_time = 0
prev_time = 0

def fingers_up(hand_landmarks, handedness):
    """Returns list: [thumb, index, middle, ring, pinky]"""

    fingers = []
    lm = hand_landmarks.landmark
    tip_ids = [4, 8, 12, 16, 20]

    if handedness == "Right":
        fingers.append(1 if lm[4].x > lm[3].x else 0)
    else:
        fingers.append(1 if lm[4].x < lm[3].x else 0)

    for tip in tip_ids[1:]:
        fingers.append(1 if lm[tip].y < lm[3].x else 0)

    return fingers 

def detect_gesture(fingers):
    """Gesture Mapping"""

    total = sum(fingers)

    if total == 5:
        return "scroll_up"
    elif total == 0:
        return "scroll_down"
    
    elif fingers == [0, 1, 0, 0, 0]:
        return "pause_toggle"
    elif fingers == [0, 1, 1, 0, 0]:
        return "none"
    
    return "none"
    
def calculate_scroll_speed(index_y):
    """Faster scrolling depending on hand height"""

    normalized = 1 - index_y
    speed = int(BASE_SCROLL_SPEED + normalized * 500)

    return max(100, min(speed, 700))

def pinch_distance(hand_landmarks):
    """Distance between thumb and index finger"""    

    thumb = hand_landmarks.landmark[4]
    index = hand_landmarks.landmark[8]

    x1, y1 = thumb.x, thumb.y
    x2, y2 = index.x, index.y

    return math.hypot(x2 - x1, y2 - y1)

print("""
      Gesture Control Started
      Open Palm -> Scroll Up
      Closed Fist -> Scroll Down
      Index Finger -> Pause/Resume
      Q -> Quit
      """)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, frame = cap.read()

    if not success:
        print("Failed to access webcam.")
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    gesture = "none"
    handedness = "Unknown"

    if results.multi_hand_landmarks:
        for hand_landmarks, hand_info in zip(
                results.multi_hand_landmarks,
                results.multi_handedness):
            handedness = hand_info.classification[0].label
            fingers = fingers_up(hand_landmarks, handedness)
            gesture = detect_gesture(fingers)
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            pinch = pinch_distance(hand_landmarks)
            if pinch < 0.05:
                gesture = "pause_toggle"

            current_time = time.time()
            if current_time - last_action_time > SCROLL_DELAY:
                index_y = hand_landmarks.landmark[8].y
                scroll_speed = calculate_scroll_speed(index_y)

                if gesture == "scroll_up" and not paused:
                    pyautogui.scroll(scroll_speed)

                elif gesture == "scroll_down" and not paused:
                    pyautogui.scroll(-scroll_speed)

                elif gesture == "pause_toggle":
                    paused = not paused
                    time.sleep(0.4)

                last_action_time = current_time

    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time else 0
    prev_time = current_time

    status_color = (0, 255, 0) if not paused else (0, 0, 255)

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Hand: {handedness}",
        (10, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )
    
    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (10, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        status_color,
        2
    )

    cv2.putText(
        frame,
        f"Paused: {paused}",
        (10, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        status_color,
        2
    )

    cv2.imshow("Advanced Gesture Scroll Control", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        paused = not paused

cap.release()
cv2.destroyAllWindows()