import odrive
import odrive.enums
from pint import UnitRegistry
from typing import Any, Optional

from config import ureg

MAX_TORQUE = 60 * ureg.newton_meter

# Type to define the input of the set method. Defines kP, kV, pDes, vDes, tDes
class MotorInput: 
    def __init__(self, kP: float = 0, kV: float = 0, pDes: float = 0, vDes: float = 0, tDes: float = 0) -> None:
        self.kP = kP
        self.kV = kV
        self.pDes = pDes
        self.vDes = vDes
        self.tDes = tDes

    def to_string(self) -> str:
        return f"MotorInput(kP={self.kP}, kV={self.kV}, pDes={self.pDes}, vDes={self.vDes}, tDes={self.tDes})"


class Motor:
    _my_drive: Optional[Any] = None

    def __init__(self, torque_bounds = (-MAX_TORQUE, MAX_TORQUE)) -> None:
        self.torque_bounds = torque_bounds
        self.motorInput = MotorInput()

    def start(self) -> None:
        self._my_drive = odrive.find_any(timeout=10)
        self._null_throw()
        self._my_drive.axis0.controller.config.control_mode = odrive.enums.ControlMode.TORQUE_CONTROL
        self._my_drive.axis0.controller.config.input_mode = odrive.enums.InputMode.PASSTHROUGH
        self._my_drive.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

    def get_state(self) -> odrive.enums.AxisState:
        """
        Get the current state of the motor.
        :return: The current state of the motor.
        """
        self._null_throw()
        # Return the current state of the motor
        return self._my_drive.axis0.current_state

    def stop(self) -> None:
        self._null_throw()
        self._my_drive.axis0.requested_state = odrive.enums.AxisState.IDLE

    def set(self, motorInput) -> None:
        self._null_throw()
        self.motorInput = motorInput
        
    def run(self, motorInput) -> None:
        """
        Run the motor with the given input.
        :param motorInput: The input to the motor.
        """
        self.set(motorInput)
        self._null_throw()
        # Set the torque using the provided input
        # Convert the torque to base units (newton-meters) and set it
        torque = motorInput.kP * (motorInput.pDes - self.get_angle().magnitude) + \
            motorInput.kV * (motorInput.vDes - self.get_velocity().magnitude) + (motorInput.tDes)
        # Constrain the torque to the specified bounds
        if torque < self.torque_bounds[0].to_base_units().magnitude:
            torque = self.torque_bounds[0].to_base_units().magnitude
        elif torque > self.torque_bounds[1].to_base_units().magnitude:
            torque = self.torque_bounds[1].to_base_units().magnitude

        self._my_drive.axis0.controller.input_torque = torque
        return torque

    @ureg.wraps(ureg.radian, (None))
    def get_angle(self) -> float:
        """
        Get the current angle of the motor.
        :return: The current angle (with units of radians).
        """
        self._null_throw()
        # Return the estimated position with units of radians
        return self._my_drive.axis0.pos_estimate * ureg.radian
    
    def get_velocity(self) -> float:
        """
        Get the current velocity of the motor.
        :return: The current velocity (with units of radians per second).
        """
        self._null_throw()
        # Return the estimated velocity with units of radians per second
        return self._my_drive.axis0.vel_estimate * ureg.radian / ureg.second
    
    def get_torque(self) -> float:
        """
        Get the current torque of the motor.
        :return: The current torque (with units of newton-meters).
        """
        self._null_throw()
        # Return the input torque with units of newton-meters
        return self._my_drive.axis0.motor.torque_estimate * ureg.newton_meter

    def _null_throw(self) -> None:
        """
        Check if the motor instance is valid. Raise an error if not.
        """
        if self._my_drive is None:
            raise ValueError("No valid motor instance")

import time
if __name__ == "__main__":
    # Example usage
    motor = Motor()
    motor.start()
    input = MotorInput(0.1, 0.01, motor.get_angle().magnitude, 0, 0)
    motor.set(input)

    # Loop until user kills, without blocking on user input
    while True:
        try:
            # Simulate a loop where we can check the motor state
            time.sleep(0.1)
            current_angle = motor.get_angle()
            current_velocity = motor.get_velocity()
            setpoint = motor.run(input)
            print(f"Current angle: {current_angle}, Current velocity: {current_velocity}, Desired torque: {setpoint}, Current torque: {motor.get_torque()}")
        except KeyboardInterrupt:
            # Stop the motor when interrupted
            motor.stop()
            print("Motor stopped.")
            break

