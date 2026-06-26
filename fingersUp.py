import cv2 as cv
import mediapipe as mp
mp_hands = mp.solutions.hands

#make a hashtable of fingers, set all to false
fingersUp = {"thumb": False, "pointer": False, "middle": False, "ring": False, "pinky": False}
currentFinger = None

finger_tips = {
    "pointer": 8,
    "middle": 12,
    "ring": 16,
    "pinky": 20
}

finger_pips = {
    "pointer": 6,
    "middle": 10,
    "ring": 14,
    "pinky": 18
}

def isFingerUp(currentFinger):
    if currentFinger in fingersUp:
        return fingersUp[currentFinger]
    else:
        return False


def determineFingerStatus(hand_landmarks):
    determineThumbStatus(hand_landmarks)
    for finger in finger_tips:

        tip_num = finger_tips[finger]
        pip_num = finger_pips[finger]

        tip_y = hand_landmarks.landmark[tip_num].y
        pip_y = hand_landmarks.landmark[pip_num].y

        fingersUp[finger] = tip_y < pip_y

def determineThumbStatus(hand_landmarks):
    tip_x = hand_landmarks.landmark[4].x
    pip_x = hand_landmarks.landmark[3].x

    fingersUp["thumb"] = tip_x < pip_x


