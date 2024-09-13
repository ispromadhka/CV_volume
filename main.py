import cv2 
import mediapipe as mp
from scipy.spatial import distance as dist
import time
import os


mp_hand = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hand.Hands(max_num_hands=4)


def distance(point1, point2):
    return dist.euclidean([point1.x, point1.y], [point2.x, point2.y])

def detect_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
    wrist = hand_landmarks.landmark[mp_hand.HandLandmark.WRIST]
    pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]

    if (distance(index_tip, wrist) < 0.12 and 
        distance(pinky_tip, wrist) < 0.12 and 
        distance(ring_finger_tip, wrist) < 0.12 and 
        distance(middle_finger_tip, wrist) < 0.12):
        return True  # fists is clenched
    return False  # fists don't clenched

# func to check hands
def get_hand(hand_landmarks, frame_width, frame_height):
    x_min, y_min = pow(10,8), pow(10,8)
    x_max, y_max = -pow(10,8), -pow(10,8)

    for lm in hand_landmarks.landmark:
        x, y = int(lm.x * frame_width), int(lm.y * frame_height)

        if x < x_min:
            x_min = x
        if y < y_min:
            y_min = y
        if x > x_max:
            x_max = x
        if y > y_max:
            y_max = y

    return x_min, y_min, x_max, y_max

cam = cv2.VideoCapture(0)
while True:
    ref, frame = cam.read()
    if not ref:
        break

    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hand.HAND_CONNECTIONS)

            if detect_gesture(hand_landmarks):
                # getting the coordinates for the hands
                x_min, y_min, x_max, y_max = get_hand(hand_landmarks, frame_width, frame_height)
                # draw a green square
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)

                time.sleep(3) 
                os.system("pkill firefox") #for linux
                break

    cv2.imshow('hands', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
