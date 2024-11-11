from pyparrot.Bebop import Bebop
from constants import TAKEOFF_COOLDOWN, LANDING_RANGE

class DroneController:
    def __init__(self):
        self.bebop = Bebop()
        self.last_takeoff_time = 0
        self.is_flying = False
        self.current_altitude = 0

    def initialize(self):
        print("Connecting")
        if self.bebop.connect(10):
            print("Success")
            self.bebop.smart_sleep(5)
            self.bebop.ask_for_state_update()
            return True
        else:
            print("Failed to connect.")
            return False

    def control_with_gesture(self, hand_sign_id, current_time):
        if hand_sign_id == 0:  # Open Hand - Takeoff or Ascend
            if not self.is_flying and current_time - self.last_takeoff_time > TAKEOFF_COOLDOWN:
                print('Open Hand - Takeoff')
                self.bebop.safe_takeoff(10)
                self.last_takeoff_time = current_time
                self.is_flying = True
                self.current_altitude = 0
            elif self.is_flying:
                print("Open Hand - Ascending")
                self.bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=50, duration=1)
                self.current_altitude += 50

        elif hand_sign_id == 1:  # Closed Hand - Descend
            if self.is_flying:
                print('Closed Hand - Descending')
                self.bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-50, duration=1)
                self.current_altitude -= 50
                if self.current_altitude <= LANDING_RANGE:
                    print('Landing command executed')
                    self.bebop.safe_land(10)
                    self.current_altitude = 0
                    self.is_flying = False

        elif hand_sign_id == 2:  # Pointing Gesture - Forward
            if self.is_flying and current_time - self.last_takeoff_time > TAKEOFF_COOLDOWN:
                print("Pointing - Going Forward")
                self.bebop.fly_direct(roll=0, pitch=50, yaw=0, vertical_movement=0, duration=1)
                self.last_takeoff_time = current_time

        elif hand_sign_id == 3:  # Ok Gesture - Backwards
            if self.is_flying and current_time - self.last_takeoff_time > TAKEOFF_COOLDOWN:
                print("Ok - Going Backwards")
                self.bebop.fly_direct(roll=0, pitch=-50, yaw=0, vertical_movement=0, duration=1)

    def disconnect(self):
        self.bebop.disconnect()
