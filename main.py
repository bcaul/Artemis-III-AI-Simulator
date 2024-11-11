import cv2
import time
import mediapipe as mp
from video_stream import VideoStream
from drone_control import DroneController
from classifier import GestureClassifier
from gesture_processing import (
    make_landmark_list, normalize_landmarks, logging_csv, 
    Get_number_pressed, make_bounding_rect, draw_bounding_rect
)
from constants import PROCESSING_INTERVAL

def main():
    # Initialize components
    drone_controller = DroneController()


    drone_active = False
    if drone_controller.initialize():
        drone_active = True
    else:
        print("Drone connection failed: Visual classifier will run WITHOUT drone.")


    classifier = GestureClassifier()
    video_stream = VideoStream(width=640, height=480, fps=15).start()

    last_processed_time = 0
    training_mode = False

    # Initialize Mediapipe hands and drawing utils
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Main loop
    running = True
    while running:
        img = video_stream.read()
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):  # ESC or 'q' to quit
            running = False
            break

        # Toggle training mode or select number if numeric key is pressed
        number, training_mode = Get_number_pressed(key, training_mode)

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
                    landmark_list = make_landmark_list(img, hand_landmarks)
                    processed_landmarks = normalize_landmarks(landmark_list)
                    
                    # Draw landmarks and bounding box
                    brect = make_bounding_rect(img, hand_landmarks)
                    draw_bounding_rect(img, brect, training_mode)
                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Log landmarks if training mode is active
                    if training_mode:
                        logging_csv(number, processed_landmarks)

                    # Predict gesture
                    gesture_id = classifier.predict(processed_landmarks)
                    
                    # Control the drone based on predicted gesture
                    if drone_active:
                        drone_controller.control_with_gesture(gesture_id, current_time)

        # Display the image with annotations
        cv2.imshow('Drone Control', img)

    # Cleanup
    drone_controller.disconnect()
    video_stream.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
