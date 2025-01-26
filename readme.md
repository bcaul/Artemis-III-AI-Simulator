# ARTEMIS III: Drone Control Simulator via Hand Gestures

This is an adaptation of the [Artemis III AI Vision](https://github.com/UoM-Robotics-Society/Artemis-III-AI-Vision). It allows the commands for the drone to be simulated in Unreal Engine 4.27 using Airsim.

This project enables a Parrot Bebop drone to be controlled via hand gestures using a live video feed and hand tracking through MediaPipe. The hand gestures are recognized and translated into commands for the drone, allowing for intuitive drone control. The project is adapted from [Kazuhito00's hand gesture recognition](https://github.com/kinivi/hand-gesture-recognition-mediapipe).

## Features

- **Real-Time Gesture Recognition**: Utilizes MediaPipe for tracking hand landmarks and TensorFlow Lite for gesture classification in real-time.
- **Drone Control**: Integrates with a Parrot Bebop drone to perform specific actions (take off, land, move forward/backward, and ascend/descend) based on recognized gestures.
- **Training Mode**: Log landmarks of hand gestures for further training or fine-tuning the classifier.

## Requirements

1. **Python 3.6 or later**: Ensure Python is installed and added to PATH.
2. **Parrot Bebop Drone** (optional): The application will run without a drone connected, allowing you to test gesture recognition without drone control.

### Dependencies

The required packages are listed in `requirements.txt`. Key dependencies include:

- `opencv-python`: For accessing webcam feed and image processing.
- `mediapipe`: For hand landmark detection.
- `numpy`: For data processing.
- `pyparrot`: To interface with the Parrot Bebop drone.
- `tensorflow`: For gesture classification model.

## Installation

1. **Clone the Repository**:

2. **Setup the Environment**:

   - Run the command below to install all necessary dependencies.

   ```bash
   python -m pip install -r requirements.txt

   ```

3. **Run the Application**:

   - Start the application by executing:

   ```bash
   python main.py

   ```

## Usage

1. **Launch the Program**: Run `main.py` as described above. The program will initialize the webcam feed, load the gesture classifier, and attempt to connect to a Parrot Bebop drone if available.
2. **Control the Drone**: Use predefined hand gestures to issue commands to the drone. Make sure gestures are within the webcam’s field of view and in clear lighting for best recognition.
3. **Exit the Program**: Press `Esc` or `q` to stop the program.

### Key Actions

- **`Esc` or `q`**: Quits the application, stopping all processes and closing the video feed.
- **`T`**: Toggles **Training Mode**. When training mode is active, you can capture hand gesture data for further model training.
- **`0-9` (Numeric Keys)**: In **Training Mode**, each number key (0-9) assigns a label to the captured gesture data. When a numeric key is pressed, the landmark data for the current gesture is saved with that numeric label to a CSV file.

## Configuration

Several constants can be configured in `constants.py`:

- `TAKEOFF_COOLDOWN`: Cooldown time between commands, in seconds.
- `LANDING_RANGE`: The distance threshold for landing.
- `PROCESSING_INTERVAL`: Time between gesture processing cycles.
- `KEYPOINT_CSV_OUTPUT_PATH` and `KEYPOINT_CLASSES`: Paths for saving landmark data and accessing labels.

Adjust these parameters to modify performance, logging, or response times.

## Gesture Mapping

Here is a list of gestures and their corresponding drone commands:

- **Open Hand**: Take off if on the ground, ascend if already flying.
- **Closed Hand**: Descend and land if the drone is close to the ground.
- **Pointing Gesture**: Move forward.
- **OK Gesture**: Move backward.

> Note: To add or modify gestures, update the model in classifier.py and adjust mappings in drone_control.py.

## Project Structure

The project is organized as follows:

- **`main.py`**: The entry point of the application, responsible for initializing and orchestrating video feed, gesture recognition, and drone control.
- **`constants.py`**: Contains adjustable configuration parameters like intervals and paths.
- **`video_stream.py`**: Handles the webcam feed as a separate threaded stream for non-blocking input.
- **`drone_control.py`**: Contains the `DroneController` class to initialize, control, and disconnect the Parrot Bebop drone based on gesture inputs.
- **`classifier.py`**: Loads and utilizes the gesture classification model, mapping gestures to numeric identifiers.
- **`gesture_processing.py`**: Provides functions for processing hand landmarks, normalizing landmarks, and logging data for training purposes.
- **`requirements.txt`**: Lists all dependencies required to run the project.

## Troubleshooting

- **No Drone Connected**: The application will still run and recognize gestures even without a drone. Make sure the Parrot Bebop drone is fully charged and connected to the same network if testing drone functionalities.
- **Gesture Recognition Issues**: Ensure there is adequate lighting, and your hand gestures are within the camera’s field of view. If recognition is inconsistent, you may need to recalibrate the model by logging more data in training mode.
- **Camera Not Detected**: Ensure that your webcam is connected and accessible by OpenCV. You may need to specify a different camera source in `VideoStream` if your system has multiple cameras.

## Credits

- **Original Gesture Recognition Code**: Adapted from [Kazuhito00's hand gesture recognition project](https://github.com/kinivi/hand-gesture-recognition-mediapipe).
- **MediaPipe**: Used for efficient hand tracking.
- **Parrot Pyparrot Library**: For easy control of Parrot Bebop drones.

This project builds on these excellent open-source tools to enable gesture-based drone control in real-time.
