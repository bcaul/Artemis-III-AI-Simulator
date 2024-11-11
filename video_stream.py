# video_stream.py
import cv2
import numpy as np
import itertools
import copy
import threading

class VideoStream:
    def __init__(self, src=0, width=320, height=240, fps=30):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.stream.set(cv2.CAP_PROP_FPS, fps)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        threading.Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()

    # Landmark processing functions
    def make_landmark_list(self, image, landmarks):
        width, height = image.shape[1], image.shape[0]
        return [[min(int(landmark.x * width), width - 1),
                 min(int(landmark.y * height), height - 1)]
                for landmark in landmarks.landmark]

    def normalize_landmarks(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)
        base_x, base_y = temp_landmark_list[0]
        for point in temp_landmark_list:
            point[0] -= base_x
            point[1] -= base_y
        max_value = max(map(abs, itertools.chain.from_iterable(temp_landmark_list)))
        return [n / max_value for n in itertools.chain.from_iterable(temp_landmark_list)]

    def make_bounding_rect(self, image, landmarks):
        width, height = image.shape[1], image.shape[0]
        landmark_array = np.empty((0, 2), int)
        for _, landmark in enumerate(landmarks.landmark):
            x = min(int(landmark.x * width), width - 1)
            y = min(int(landmark.y * height), height - 1)
            landmark_point = [np.array((x, y))]
            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv2.boundingRect(landmark_array)
        return [x, y, x + w, y + h]

    def draw_bounding_rect(self, image, brect, training_mode):
        if brect:
            color = (0, 255, 0) if training_mode else (255, 0, 0)
            cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), color, 1)
