import cv2
import mediapipe as mp
import math
import numpy as np
import serial
import time
from fingersUp import determineFingerStatus, fingersUp


# Initialize webcam and MediaPipe Hands
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
pinch = False
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
prev_x, prev_y = None, None
smooth_x, smooth_y = 0,0
alpha = 0.2
global distance

#arduino side
last_state = None
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

arduino.write(b'1\n')

#initialize drawing
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
drawing = False

#set window size
cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)

cv2.resizeWindow("Hand Tracking", 1000, 700)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    
    h,w,c = frame.shape

    # Flip the frame horizontally for a mirror view & convert to RGB
    image = cv2.flip(frame, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image and find hands
    results = hands.process(image_rgb)

    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            determineFingerStatus(hand_landmarks)

        lm4 = hand_landmarks.landmark[4] #thumb end
        lm8 = hand_landmarks.landmark[8] #pointer end

        #set coordinates
        x4, y4 = lm4.x, lm4.y
        x8, y8 = lm8.x, lm8.y 
    
        distance = math.sqrt((x8 - x4)**2 + (y8-y4)**2)

        #find pixel coordinates from given x and y coordinates
        px = int(x4 * w)
        py = int(y4 * h)

        # Smooth coordinates
        smooth_x = int(alpha * px + (1 - alpha) * smooth_x)
        smooth_y = int(alpha * py + (1 - alpha) * smooth_y)

        fingerOrder = ["thumb", "pointer", "middle", "ring", "pinky"]
        data = "" #string that is sent to arduino

        for finger in fingerOrder:
            if fingersUp[finger]:
                data += '1'
            else:
                data += '0'
        if data != last_state:
            arduino.write((data + '\n').encode())
            print(data.encode())
            last_state = data

        # for finger,status in fingersUp.items():
        #      if status:
        #          data += "1" #if true, send 1 (on)
        #      else:
        #          data += "0" #if false, sense 0 (off)
        #arduino.write((data + '\n').encode())
        #print(data.encode())



        #check if fingers are close to each other
        # if distance < 0.05: #if yes then draw line
        #     pinch = True
        #     drawing = True
        #     cv2.circle(canvas, (smooth_x,smooth_y), 5, (0,255,0), -1)

        #     if last_state != "ON":
        #         arduino.write(b'LED_ON\n')
        #         last_state = "ON"

        # else:
        #     pinch = False
        #     drawing = False
        #     prev_x, prev_y = None, None

        #     if last_state != "OFF":
        #         #arduino.write(b'LED_OFF\n')
        #         last_state = "OFF"
        
            

    # Display the output
    combined = cv2.add(canvas, image)

    cv2.imshow('Hand Tracking', combined)
    #print(pinch)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

cap.release()
cv2.destroyAllWindows()
