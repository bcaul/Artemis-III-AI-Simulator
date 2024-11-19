from pyparrot.Bebop import Bebop
from constants import TAKEOFF_COOLDOWN, LANDING_RANGE


class DroneController:
    def __init__(self):
        self.bebop = Bebop()
        self.last_takeoff_time = 0
        self.is_flying = False
        self.current_altitude = 0

    def initialize(self):
        """Connect to the drone and initialize its state."""
        print("Connecting to drone...")
        if self.bebop.connect(10):
            print("Connected successfully.")
            self.bebop.smart_sleep(5)
            self.bebop.ask_for_state_update()
            return True
        else:
            print("Failed to connect.")
            return False

    def can_take_action(self, current_time):
        """Check if the cooldown period has elapsed."""
        return current_time - self.last_takeoff_time > TAKEOFF_COOLDOWN
    
    def emergency_stop(self, key, current_time):
        """Causes an immediate landing if the space button is pressed"""
        if key == 32:
            print ("Emergency Landing Triggered, Landing Immediately")
            self.bebop.safe_land(10)
            self.is_flying = False
            self.current_altitude = 0
            self.last_takeoff_time = current_time #Prevents further actions until cooldown period is over
        else:
            print ("Drone is not flying. No emergency stop required")

    def takeoff_or_ascend(self, current_time):
        """Handle takeoff or ascending actions based on current state."""
        if not self.is_flying and self.can_take_action(current_time):
            print("Open Hand - Takeoff")
            self.bebop.safe_takeoff(10)
            self.is_flying = True
            self.current_altitude = 0
        elif self.is_flying:
            print("Open Hand - Ascending")
            self.bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=50, duration=1)
            self.current_altitude += 50
        self.last_takeoff_time = current_time

    def descend_or_land(self):
        """Handle descending or landing actions based on altitude."""
        if self.is_flying:
            print("Closed Hand - Descending")
            self.bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-50, duration=1)
            self.current_altitude -= 50
            if self.current_altitude <= LANDING_RANGE:
                print("Landing command executed")
                self.bebop.safe_land(10)
                self.current_altitude = 0
                self.is_flying = False

    def move_forward(self, current_time):
        """Move the drone forward if flying and cooldown has passed."""
        if self.is_flying and self.can_take_action(current_time):
            print("Pointing - Going Forward")
            self.bebop.fly_direct(roll=0, pitch=-50, yaw=0, vertical_movement=0, duration=1)
            self.last_takeoff_time = current_time

    def move_backward(self, current_time):
        """Move the drone backward if flying and cooldown has passed."""
        if self.is_flying and self.can_take_action(current_time):
            print("Ok - Going Backwards")
            self.bebop.fly_direct(roll=0, pitch=50, yaw=0, vertical_movement=0, duration=1)
            self.last_takeoff_time = current_time

    def rotate_clockwise(self, current_time):
        """Rotate the drone clockwise if flying and cooldown has passed."""
        if self.is_flying and self.can_take_action(current_time):
            print ("Peace Sign - Rotating Clockwise")
            self.bebop.fly_direct(roll=0, pitch = 0, yaw= 50, vertical_movement=0, duration=1) 
            self.last_takeoff_time = current_time

    def rotate_counter_clockwise(self, current_time):
        """Rotate the drone counter-clockwise if flying and cooldown has passed."""
        if self.is_flying and self.can_take_action(current_time):
            print ("Shaka - Rotating Clockwise")
            self.bebop.fly_direct(roll=0, pitch = 0, yaw= -50, vertical_movement=0, duration=1) 
            self.last_takeoff_time = current_time

    def flip(self, current_time):
        """Flip the Drone"""
        if self.is_flying and self.can_take_action(current_time):
            print ("Peace Among Worlds - Frontflip")
            self.bebop.flip("front")
            self.last_takeoff_time = current_time


    def control_with_gesture(self, hand_sign_id, current_time):
        """Control the drone based on the detected gesture."""
        actions = {
            0: self.takeoff_or_ascend,
            1: self.descend_or_land,
            2: self.move_forward,
            3: self.move_backward,
            4: self.rotate_clockwise,
            5: self.rotate_counter_clockwise,
            6: self.flip
        }
        
        action = actions.get(hand_sign_id)
        if action:
            action(current_time)

    def disconnect(self):
        """Disconnect from the drone."""
        self.bebop.disconnect()
