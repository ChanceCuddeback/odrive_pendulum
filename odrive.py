import odrive
import odrive.enums
from typing import Any, Optional

class Motor:
    _my_drive : Optional[Any] = None

    def start(self) -> None:
        self._my_drive = odrive.find_any()
        self._my_drive.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

    def stop_drive(self):
        if self._my_drive == None:
            return
        self._my_drive.axis0.requested_state = odrive.enums.AxisState.IDLE

    def move_to(self, angle):
        self._my_drive.axis0.controller.input_pos = angle