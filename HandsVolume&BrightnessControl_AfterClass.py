import cv2
import mediapipe as mp
import numpy as np
import os
import platform
import time

OS = platform.system()

if OS != "Darwin":
    print("⚠️ This project is designed for macOS.")

    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
draw = mp.solutions.drawing_utils

THUMB = mp_hands.HandLandmark.THUMB_TIP
INDEX = mp_hands.HandLandmark.INDEX_FINGER_TIP

last_volume = -1
last_brightness = -1

def set_volume(percent):
    global last_volume

    percent = int(np.clip(percent, 0, 100))

    if abs(percent - last_volume) >= 2:
        os.system(
            f"osascript -e 'set volume output volume {percent}'"
        )
        last_volume = percent

current_brightness = 50

def set_brightness(percent):
   global current_brightness

   percent = int(max(0, min(100, percent)))
   difference = percent - current_brightness

   if difference > 5:
    presses = difference // 5

    for _ in range(presses):
        os.system("""
        osascript -e 'tell application "System Events"
            key code 144
        end tell'
        """)

   elif difference < -5:
    presses = abs(difference) // 5

    for _ in range(presses):
        os.system("""
        osascript -e 'tell application "System Events"
            key code 145
        end tell'
        """)

    current_brightness = percent

cap = cv2.VideoCapture(0)

if not cap.isOpened():
   print("Could not access camera.")
   exit()

WINDOW = "Hand Gesture Controller"

cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)

prev_time = 0

while True:
   success, img = cap.read()

   if not success:
      break
   
   img = cv2.flip(img, 1)
   h, w = img.shape[:2]
   rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   result = hands.process(rgb)

   if result.multi_hand_landmarks and result.multi_handedness:
      for i, hand_landmarks in enumerate(result.multi_hand_landmarks):
         label = result.multi_handedness[i].classification[0].label

         draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
         lm = hand_landmarks.landmark

         thumb = (
                int(lm[THUMB].x * w),
                int(lm[THUMB].y * h)
            )

         index = (
                int(lm[INDEX].x * w),
                int(lm[INDEX].y * h)
            )
         
         cv2.circle(img, thumb, 10, (255, 0, 255), cv2.FILLED)
         cv2.circle(img, index, 10, (255, 0, 255), cv2.FILLED)
         cv2.line(img, thumb, index, (0, 255, 0), 3)

         dist = np.hypot(
                index[0] - thumb[0],
                index[1] - thumb[1]
            )
         percent = np.interp(dist, [30, 250], [0, 100])
         percent = int(np.clip(percent, 0, 100))

         bar = int(np.interp(percent, [0, 100], [400, 150]))

         if label == "Left":
            set_volume(percent)
            cv2.rectangle(
                    img,
                    (50, 150),
                    (90, 400),
                    (255, 0, 0),
                    3
                )
            cv2.rectangle(
                    img,
                    (50, bar),
                    (90, 400),
                    (255, 0, 0),
                    cv2.FILLED
                )
            cv2.putText(
                    img,
                    f"VOL {percent}%",
                    (25, 430),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    3
                )
            
         elif label == "Right":
            set_brightness(percent)
            
            x1 = w - 90
            x2 = w - 50

            cv2.rectangle(
                    img,
                    (x1, 150),
                    (x2, 400),
                    (0, 255, 0),
                    3
                )
            cv2.rectangle(
                    img,
                    (x1, bar),
                    (x2, 400),
                    (0, 255, 0),
                    cv2.FILLED
                )
            
            cv2.putText(
                    img,
                    f"BRT {percent}%",
                    (w - 200, 430),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )
            
   current_time = time.time()

   fps = 1 / (current_time - prev_time) if prev_time != 0 else 0

   prev_time = current_time

   cv2.putText(
        img,
        f"FPS: {int(fps)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )
   
   cv2.imshow(WINDOW, img)

   key = cv2.waitKey(1) & 0xFF

   if key == ord("q"):
      break
   
cap.release()
cv2.destroyAllWindows()
