import csv
from Model.Keypoint_classifier import KeyPointClassifier
from constants import KEYPOINT_LABEL_CSV_PATH

def load_keypoint_labels():
    with open(KEYPOINT_LABEL_CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]

class GestureClassifier:
    def __init__(self):
        self.classifier = KeyPointClassifier()
        self.labels = load_keypoint_labels()

    def predict(self, landmark_list):
        # Calls the KeyPointClassifier instance to get a prediction
        return self.classifier(landmark_list)
