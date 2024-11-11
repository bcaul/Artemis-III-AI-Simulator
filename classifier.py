from Model.Keypoint_classifier import KeyPointClassifier
from constants import KEYPOINT_CLASSES


# classifier.py
from constants import KEYPOINT_CLASSES

class GestureClassifier:
    def __init__(self):
        self.classifier = KeyPointClassifier()
    
    def predict(self, landmark_list):
        # Get the gesture ID and return the corresponding label from KEYPOINT_CLASSES
        gesture_id = self.classifier(landmark_list)
        return KEYPOINT_CLASSES.get(gesture_id, "Unknown")  # Return "Unknown" if gesture_id not found
