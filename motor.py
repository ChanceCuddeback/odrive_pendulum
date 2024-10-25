import odrive
import odrive.enums
from typing import Any, Optional

class Motor:
    _my_drive : Optional[Any] = None

    def start(self) -> None:
        self._my_drive = odrive.find_any()
        self._my_drive.axis0.requested_state = odrive.enums.ControlMode.TORQUE_CONTROL

    def stop(self) -> None:
        if self._null_guard():
            return
        self._my_drive.axis0.requested_state = odrive.enums.AxisState.IDLE

    def move_to(self, angle) -> None:
        if self._null_guard():
            return
        self._my_drive.axis0.controller.input_pos = angle

    def set_torque(self, torque) -> None:
        if self._null_guard():
            return
        self._my_drive.axis0.controller.input_torque = torque

    def get_angle(self) -> float:
        if self._null_guard():
            return
        return self._my_drive.axis0.pos_estimate

    def _null_guard(self) -> bool:
        return self._my_drive == None
