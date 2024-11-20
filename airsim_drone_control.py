import airsim
import time
import math
from constants import TAKEOFF_COOLDOWN, LANDING_RANGE

class DroneController:
    def __init__(self):
        self.client = None
        self.is_flying = False
        self.last_takeoff_time = 0
        self.current_altitude = 0
        self.current_yaw = 0  # Track the drone's yaw (rotation)

    def initialize(self):
        """Connect to AirSim and initialize the drone."""
        try:
            self.client = airsim.MultirotorClient()  # Connect to AirSim (default IP: localhost)
            self.client.confirmConnection()
            print("Connected to AirSim!")
            self.client.enableApiControl(True)  # Enable API control
            self.client.armDisarm(True)  # Arm the drone
            print("Drone armed and ready.")
            return True
        except Exception as e:
            print(f"Failed to connect to AirSim: {e}")
            self.client = None
            return False

    def can_take_action(self, current_time):
        """Check if enough time has passed since the last action."""
        return current_time - self.last_takeoff_time > TAKEOFF_COOLDOWN

    def takeoff_or_ascend(self, current_time):
        """Handle takeoff or ascending actions."""
        if not self.is_flying and self.can_take_action(current_time):
            print("Open Hand - Taking Off")
            try:
                self.client.takeoffAsync().join()
                self.is_flying = True
                self.current_altitude = 2  # Initial altitude
                self.last_takeoff_time = current_time
            except Exception as e:
                print(f"Error during takeoff: {e}")
        elif self.is_flying:
            print("Open Hand - Ascending")
            try:
                self.client.moveByVelocityAsync(0, 0, -5, 2).join()  # Move upward
                self.current_altitude += 10
                self.last_takeoff_time = current_time
            except Exception as e:
                print(f"Error during ascent: {e}")

    def descend_or_land(self, current_time):
        """Handle descending or landing actions."""
        if self.is_flying:
            print("Closed Hand - Descending or Landing")
            try:
                self.client.moveByVelocityAsync(0, 0, 5, 2).join()  # Move downward
                self.current_altitude -= 10
                if self.current_altitude <= LANDING_RANGE:
                    print("Landing...")
                    self.client.landAsync().join()
                    self.is_flying = False
                    self.current_altitude = 0
            except Exception as e:
                print(f"Error during descent or landing: {e}")

    def move_forward(self, current_time):
        """Move forward in the drone's current orientation."""
        if self.is_flying and self.can_take_action(current_time):
            print("Pointing - Moving Forward")
            try:
                # Move the drone forward in its current facing direction
                velocity_x = 5 * math.cos(math.radians(self.current_yaw))  # Adjust for yaw (rotation)
                velocity_y = 5 * math.sin(math.radians(self.current_yaw))  # Adjust for yaw (rotation)
                self.client.moveByVelocityAsync(velocity_x, velocity_y, 0, 2).join()  # Move horizontally in direction of rotation
                self.last_takeoff_time = current_time
            except Exception as e:
                print(f"Error moving forward: {e}")

    def move_backward(self, current_time):
        """Move backward in the drone's current orientation."""
        if self.is_flying and self.can_take_action(current_time):
            print("OK - Moving Backward")
            try:
                # Move the drone backward in its current facing direction
                velocity_x = -5 * math.cos(math.radians(self.current_yaw))  # Adjust for yaw (rotation)
                velocity_y = -5 * math.sin(math.radians(self.current_yaw))  # Adjust for yaw (rotation)
                self.client.moveByVelocityAsync(velocity_x, velocity_y, 0, 2).join()  # Move horizontally in direction of rotation
                self.last_takeoff_time = current_time
            except Exception as e:
                print(f"Error moving backward: {e}")

    def rotate_clockwise(self, current_time):
        """Rotate clockwise."""
        if self.is_flying and self.can_take_action(current_time):
            print("Peace Sign - Rotating Clockwise")
            try:
                self.client.rotateByYawRateAsync(30, 2).join()
                self.current_yaw += 30  # Update yaw after rotation
                self.last_takeoff_time = current_time
            except Exception as e:
                print(f"Error rotating clockwise: {e}")

    def rotate_counter_clockwise(self, current_time):
        """Rotate counter-clockwise."""
        if self.is_flying and self.can_take_action(current_time):
            print("Shaka - Rotating Counterclockwise")
            try:
                self.client.rotateByYawRateAsync(-30, 2).join()
                self.current_yaw -= 30  # Update yaw after rotation
                self.last_takeoff_time = current_time
            except Exception as e:
                print(f"Error rotating counterclockwise: {e}")

    def flip(self, current_time):
        """Perform a front flip."""
        if self.is_flying and self.can_take_action(current_time):
            print("Peace Among Worlds - Performing Flip")
            try:
                self.client.moveByVelocityAsync(0, 0, 2, 1).join()
                self.client.moveByVelocityAsync(0, 0, -2, 1).join()
                self.last_takeoff_time = current_time
            except Exception as e:
                print(f"Error performing flip: {e}")

    def control_with_gesture(self, gesture_id, current_time):
        """Control the drone using the detected gesture."""
        actions = {
            0: self.takeoff_or_ascend,
            1: self.descend_or_land,
            2: self.move_forward,
            3: self.move_backward,
            4: self.rotate_clockwise,
            5: self.flip,
            6: self.rotate_counter_clockwise
        }
        action = actions.get(gesture_id)
        if action:
            action(current_time)

    def disconnect(self):
        """Release control and disarm the drone."""
        if self.client:
            try:
                self.client.armDisarm(False)
                self.client.enableApiControl(False)
                print("Drone disconnected.")
            except Exception as e:
                print(f"Error during disconnection: {e}")
