from unittest.mock import MagicMock, patch
from src.motor import Motor
from src.config import ureg

@patch("odrive.find_any", return_value=MagicMock())  # Mock odrive.find_any
def test_motor_start(mock_find_any):
    motor = Motor()
    motor.start()

    # Assert that odrive.find_any was called
    mock_find_any.assert_called_once()

    # Check that the motor is set to torque control mode
    motor._my_drive.axis0.requested_state = MagicMock()
    motor._my_drive.axis0.requested_state = 1  # Mocked value for torque control

def test_motor_get_angle():
    motor = Motor()
    motor._my_drive = MagicMock()
    motor._my_drive.axis0.pos_estimate = 1.0

    angle = motor.get_angle()
    assert angle.magnitude == 1.0