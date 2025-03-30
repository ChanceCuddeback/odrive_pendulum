import odrive
import odrive.enums
from pint import UnitRegistry
from typing import Any, Optional

from config import ureg
from utils import ewma

MAX_TORQUE = 5 * ureg.newton_meter

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

    def start(self, watchdog_timeout = 0.5) -> None:
        self._my_drive = odrive.find_any(timeout=10)
        self._null_throw()

        #TODO: Setup anti-cogging

        self._my_drive.axis0.config.enable_watchdog = watchdog_timeout > 0
        self._my_drive.axis0.config.watchdog_timeout = watchdog_timeout
        self._my_drive.axis0.controller.config.control_mode = odrive.enums.ControlMode.TORQUE_CONTROL
        self._my_drive.axis0.controller.config.enable_torque_mode_vel_limit = True
        self._my_drive.axis0.controller.config.vel_limit = 3 # rev / s
        self._my_drive.axis0.controller.config.input_mode = odrive.enums.InputMode.PASSTHROUGH
        self._my_drive.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL
        self._my_drive.axis0.controller.input_torque = 0
        self.pet()

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
        self.prior_torque = motorInput.tDes
        
    def run(self, motorInput, alpha=1.0) -> None: 
        """
        Run the motor with the given input.
        :param motorInput: The input to the motor.
        """
        # TODO: Add windmilling
        self.set(motorInput)
        self._null_throw()
        # Set the torque using the provided input

        torque = motorInput.kP * (motorInput.pDes - self.get_angle().magnitude) + \
            motorInput.kV * (motorInput.vDes - self.get_velocity().magnitude) + (motorInput.tDes)

        if torque < self.torque_bounds[0].to_base_units().magnitude:
            torque = self.torque_bounds[0].to_base_units().magnitude
        elif torque > self.torque_bounds[1].to_base_units().magnitude:
            torque = self.torque_bounds[1].to_base_units().magnitude

        torque = ewma(torque, self.prior_torque, alpha)
        self._my_drive.axis0.controller.input_torque = torque
        self.prior_torque = torque

        self.pet()
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
    
    def pet(self) -> None:
        """
        Feed the watchdog to prevent the motor from going into idle state.
        """
        self._null_throw()
        try:
            self._my_drive.axis0.watchdog_feed()
        except Exception as e:
            print(e)

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
    input = MotorInput(1, -0.01, motor.get_angle().magnitude, 0, 0)
    motor.set(input)

    # Loop until user kills, without blocking on user input
    while True:
        try:
            # Simulate a loop where we can check the motor state
            current_angle = motor.get_angle()
            current_velocity = motor.get_velocity()
            setpoint = motor.run(input)
            print(f"Desired torque: {setpoint}, Current torque: {motor.get_torque()}")
            time.sleep(0.01)
        except KeyboardInterrupt:
            # Stop the motor when interrupted
            motor.stop()
            print("Motor stopped.")
            break

