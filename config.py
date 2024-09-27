#!/usr/bin/env python3 #TODO Figure out why odrive.enums cannot import in this directory
import odrive
import time
import math

import odrive.enums

def get_first_drive():
    return odrive.find_any()
    
def set_config(odrv):
    odrv.config.dc_bus_overvoltage_trip_level = 25
    odrv.config.dc_bus_undervoltage_trip_level = 10.5
    odrv.config.dc_max_positive_current = 30
    odrv.config.dc_max_negative_current = -10
    odrv.axis0.config.motor.motor_type = odrive.enums.MotorType.HIGH_CURRENT
    odrv.axis0.config.motor.pole_pairs = 20
    odrv.axis0.config.motor.torque_constant = 0.0827
    odrv.axis0.config.motor.current_soft_max = 50
    odrv.axis0.config.motor.current_hard_max = 70
    odrv.axis0.config.motor.calibration_current = 10
    odrv.axis0.config.motor.resistance_calib_max_voltage = 2
    odrv.axis0.config.calibration_lockin.current = 10
    odrv.axis0.motor.motor_thermistor.config.enabled = False
    odrv.axis0.controller.config.control_mode = odrive.enums.ControlMode.POSITION_CONTROL
    odrv.axis0.controller.config.input_mode = odrive.enums.InputMode.POS_FILTER
    odrv.axis0.controller.config.vel_limit = 50
    odrv.axis0.controller.config.vel_limit_tolerance = 1.1
    odrv.axis0.config.torque_soft_min = -math.inf
    odrv.axis0.config.torque_soft_max = math.inf
    odrv.axis0.controller.config.input_filter_bandwidth = 20
    odrv.can.config.protocol = odrive.enums.Protocol.NONE
    odrv.axis0.config.enable_watchdog = False
    odrv.axis0.config.load_encoder = odrive.enums.EncoderId.ONBOARD_ENCODER0
    odrv.axis0.config.commutation_encoder = odrive.enums.EncoderId.ONBOARD_ENCODER0
    odrv.config.enable_uart_a = False

def save_to_nvm(odrv):
    odrv.save_configuration()
    time.sleep(1)

def calibrate(odrv):
    odrv.axis0.requested_state = odrive.enums.AxisState.FULL_CALIBRATION_SEQUENCE
    while odrv.axis0.current_state != odrive.enums.AxisState.IDLE:
        time.sleep(0.1)


drv = odrive.find_any()
set_config(drv)
save_to_nvm(drv)
drv.reboot()
time.sleep(2)
calibrate(drv)
save_to_nvm(drv)
drv.reboot()
time.sleep(2)