# main.py
import cv2
import time
import mediapipe as mp
from Model.Keypoint_classifier import KeyPointClassifier
from video_stream import VideoStream
from drone_control import DroneController
from gesture_processing import logging_csv
from constants import KEYPOINT_CLASSES, PROCESSING_INTERVAL

def main():
    # Initialize the drone
    drone_controller = DroneController()
    drone_active = drone_controller.initialize()

    video_stream = VideoStream(width=640, height=480, fps=15).start()

    last_processed_time = 0
    training_mode = False

    # Initialize Mediapipe hands and drawing utils
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Initialize KeyPointClassifier
    keypoint_classifier = KeyPointClassifier()

    # Main loop
    while True:
        img = video_stream.read()
        key = cv2.waitKey(10)

        # ESC or 'q' to quit
        if key == 27 or key == ord('q'):
            video_stream.stop()
            break

        # 't' toggles training mode
        if key == ord('t'): 
            training_mode = not training_mode

        # Process gestures at regular intervals
        current_time = time.time()
        if current_time - last_processed_time > PROCESSING_INTERVAL:
            last_processed_time = current_time
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Process image for hand landmarks
            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Generate landmark list and process landmarks
                    landmark_list = video_stream.make_landmark_list(img, hand_landmarks)
                    processed_landmarks = video_stream.normalize_landmarks(landmark_list)
                    
                    # Draw landmarks and bounding box
                    brect = video_stream.make_bounding_rect(img, hand_landmarks)
                    video_stream.draw_bounding_rect(img, brect, training_mode)
                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Log landmarks if training mode is active
                    if training_mode: 
                        logging_csv(key, processed_landmarks)

                    # Classify the gesture
                    try:
                        gesture_id = keypoint_classifier(processed_landmarks)  # Pass processed landmarks
                        gesture_name = KEYPOINT_CLASSES.get(gesture_id, "Unknown")  # Return "Unknown" if gesture_id not found
                        print(f"Detected gesture: {gesture_name}")
                    except ValueError as e:
                        print("Error during classification:", e)
                        gesture_name = "Error"

                    # Display detected gesture on the video stream
                    cv2.putText(img, f"Gesture: {gesture_name}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Control the drone based on predicted gesture
                    if drone_active:
                        drone_controller.control_with_gesture(gesture_name, current_time)

        # Display the image with annotations
        cv2.imshow('Drone Control', img)

    # Cleanup
    if drone_active: 
        drone_controller.disconnect()
    video_stream.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
