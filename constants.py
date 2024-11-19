# constants.py
TAKEOFF_COOLDOWN = 1.0  # Cool down period between inputs (seconds)
LANDING_RANGE = 50      # Landing range (in cm)
PROCESSING_INTERVAL = 0.01  # Time between processing  (seconds)
KEYPOINT_CSV_OUTPUT_PATH = 'Model/keypoint.csv'
KEYPOINT_CLASSES = {
    0: "Open",
    1: "Closed fist",
    2: "Pointer",
    3: "OK",
    4: "Peace sign",
    5: "F Finger",
    6: "Shaka"
}


