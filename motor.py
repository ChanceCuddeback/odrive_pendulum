import odrive
from odrive.enums import *
from typing import Any, Optional

class Motor:
    _my_drive : Optional[Any] = None

    def start(self) -> None:
        self._my_drive = odrive.find_any()
        self._my_drive.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

    def stop_drive(self):
        if self._null_guard(self):
            return
        self._my_drive.axis0.requested_state = odrive.enums.AxisState.IDLE

    def move_to(self, angle):
        if self._null_guard(self):
            return
        self._my_drive.axis0.controller.input_pos = angle

    def _null_guard(self) -> bool:
        return self._my_drive == None
