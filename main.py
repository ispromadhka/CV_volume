import cv2 
import mediapipe as mp

mp_hand = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hand.Hands()

cam = cv2.VideoCapture(0)

while True:
    ref ,frame = cam.read()
    if not ref:
        break

    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,hand_landmarks,mp_hand.HAND_CONNECTIONS)
    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()