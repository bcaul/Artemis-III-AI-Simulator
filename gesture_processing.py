# gesture_processing.py
import itertools
import numpy as np
import copy
import csv
import cv2
from constants import KEYPOINT_CSV_PATH

def make_landmark_list(image, landmarks):
    width, height = image.shape[1], image.shape[0]
    return [[min(int(landmark.x * width), width - 1),
             min(int(landmark.y * height), height - 1)]
            for landmark in landmarks.landmark]

def normalize_landmarks(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)
    base_x, base_y = temp_landmark_list[0]
    for point in temp_landmark_list:
        point[0] -= base_x
        point[1] -= base_y
    max_value = max(map(abs, itertools.chain.from_iterable(temp_landmark_list)))
    return [n / max_value for n in itertools.chain.from_iterable(temp_landmark_list)]

def logging_csv(number, landmark_list):
    if 0 <= number <= 9:
        with open(KEYPOINT_CSV_PATH, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *landmark_list])

def Get_number_pressed(key, training):
    number = -1
    if 48 <= key <= 57:  # Keys 0-9
        number = key - 48
    elif key == ord('t'):  # 't' toggles training mode
        training = not training
    return number, training

def make_bounding_rect(image, landmarks):
    """Creates a bounding rectangle around the hand landmarks."""
    width, height = image.shape[1], image.shape[0]
    landmark_array = np.empty((0, 2), int)
    for _, landmark in enumerate(landmarks.landmark):
        x = min(int(landmark.x * width), width - 1)
        y = min(int(landmark.y * height), height - 1)
        landmark_point = [np.array((x, y))]
        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv2.boundingRect(landmark_array)
    return [x, y, x + w, y + h]

def draw_bounding_rect(image, brect, training_mode):
    """Draws a bounding rectangle around detected hand landmarks."""
    if brect:
        color = (0, 255, 0) if training_mode else (255, 0, 0)
        cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), color, 1)
