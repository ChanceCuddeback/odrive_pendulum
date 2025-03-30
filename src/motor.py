import odrive
import odrive.enums
from pint import UnitRegistry
from typing import Any, Optional

from src.config import ureg

class Motor:
    _my_drive: Optional[Any] = None

    def start(self) -> None:
        self._my_drive = odrive.find_any(timeout=10)
        self._null_throw()
        self._my_drive.axis0.requested_state = odrive.enums.ControlMode.TORQUE_CONTROL

    def stop(self) -> None:
        self._null_throw()
        self._my_drive.axis0.requested_state = odrive.enums.AxisState.IDLE

    @ureg.wraps(None, (None, ureg.radian))
    def move_to(self, angle) -> None:
        """
        Move the motor to a specific angle.
        :param angle: The target angle (with units of radians).
        """
        self._null_throw()
        # Convert the angle to base units (radians) and set it
        self._my_drive.axis0.controller.input_pos = angle

    @ureg.wraps(None, (None, ureg.newton_meter))
    def set_torque(self, torque) -> None:
        """
        Set the torque for the motor.
        :param torque: The torque to apply (with units of newton-meters).
        """
        self._null_throw()
        print("Got torque:", torque)
        # Convert the torque to base units (newton-meters) and set it
        self._my_drive.axis0.controller.input_torque = torque

    @ureg.wraps(ureg.radian, (None))
    def get_angle(self) -> float:
        """
        Get the current angle of the motor.
        :return: The current angle (with units of radians).
        """
        self._null_throw()
        # Return the estimated position with units of radians
        return self._my_drive.axis0.pos_estimate * ureg.radian

    def _null_throw(self) -> None:
        """
        Check if the motor instance is valid. Raise an error if not.
        """
        if self._my_drive is None:
            raise ValueError("No valid motor instance")
