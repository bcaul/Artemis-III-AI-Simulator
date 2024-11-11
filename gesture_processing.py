# gesture_processing.py
import csv
from constants import KEYPOINT_CSV_OUTPUT_PATH, KEYPOINT_CLASSES

def logging_csv(key, landmark_list):
    number_hit = -1
    if 48 <= key <= 57:  # Keys 0-9
      number_hit = key - 48
    # Only log data if the label number exists in KEYPOINT_CLASSES
    if number_hit in KEYPOINT_CLASSES:
        with open(KEYPOINT_CSV_OUTPUT_PATH, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number_hit, *landmark_list])