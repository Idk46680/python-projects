import cv2
import mediapipe as mp
import numpy as np
import os
import platform


OS = platform.system()
if OS != "Darwin":
    print("⚠️ This version is for macOS only.")


Hands = mp.solutions.hands
hands = Hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

draw = mp.solutions.drawing_utils

TH = Hands.HandLandmark.THUMB_TIP
IX = Hands.HandLandmark.INDEX_FINGER_TIP


def set_volume(percent):
    percent = max(0, min(100, percent))
    os.system(f"osascript -e 'set volume output volume {percent}'")


def set_brightness(percent):
    percent = max(0, min(100, percent))
    os.system(f"brightness {percent/100}")


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Webcam not accessible")
    exit()

WIN = "Hand Gesture Control (Mac)"
cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)


while True:

    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w = img.shape[:2]

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks and result.multi_handedness:

        for i, hand in enumerate(result.multi_hand_landmarks):

            label = result.multi_handedness[i].classification[0].label

            draw.draw_landmarks(
                img,
                hand,
                Hands.HAND_CONNECTIONS
            )

            lm = hand.landmark

            thumb = (int(lm[TH].x * w), int(lm[TH].y * h))
            index = (int(lm[IX].x * w), int(lm[IX].y * h))

            cv2.circle(img, thumb, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, index, 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, thumb, index, (0, 255, 0), 3)

            # distance between fingers
            dist = np.hypot(index[0] - thumb[0],
                            index[1] - thumb[1])

            percent = int(np.interp(dist, [30, 300], [0, 100]))

            # -----------------------------
            # LEFT HAND → VOLUME
            # -----------------------------
            if label == "Left":

                set_volume(percent)

                bar = int(np.interp(dist, [30, 300], [400, 150]))

                cv2.rectangle(img, (50,150), (85,400),
                              (255,0,0), 2)
                cv2.rectangle(img, (50,bar), (85,400),
                              (255,0,0), cv2.FILLED)

                cv2.putText(img,
                            f"VOL {percent}%",
                            (30,450),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255,0,0),
                            3)

         
            elif label == "Right":

                set_brightness(percent)

                bar = int(np.interp(dist, [30, 300], [400, 150]))
                x1, x2 = w-85, w-50

                cv2.rectangle(img, (x1,150), (x2,400),
                              (0,255,0), 2)
                cv2.rectangle(img, (x1,bar), (x2,400),
                              (0,255,0), cv2.FILLED)

                cv2.putText(img,
                            f"BRT {percent}%",
                            (w-150,450),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0,255,0),
                            3)

    cv2.imshow(WIN, img)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()