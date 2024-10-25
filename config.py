#!/usr/bin/env python3 #TODO Figure out why odrive.enums cannot import in this directory
import odrive
import time
import math

import odrive.enums

def get_drive():
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
    odrv.axis0.controller.config.control_mode = odrive.enums.ControlMode.TORQUE_CONTROL
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
    # manual changes for absolute reference frame 
    odrv.axis0.pos_vel_mapper.config.offset = 0.0
    odrv.axis0.pos_vel_mapper.config.offset_valid = True
    odrv.axis0.pos_vel_mapper.config.approx_init_pos = 0.0
    odrv.axis0.pos_vel_mapper.config.approx_init_pos_valid = True
    odrv.axis0.controller.config.absolute_setpoints = True
    # manual changes for anti-cogging
    odrv.axis0.controller.config.vel_gain = 1.0
    odrv.axis0.config.anticogging.max_torque = 1.2
    odrv.axis0.config.anticogging.calib_start_vel = 0.5
    odrv.axis0.config.anticogging.calib_end_vel = 0.05
    odrv.axis0.config.anticogging.calib_coarse_integrator_gain = 25
    odrv.axis0.config.anticogging.enabled = True


def save_to_nvm(odrv):
    odrv.axis0.requested_state = odrive.enums.AxisState.IDLE
    try:
        odrv.save_configuration()
    finally:
        time.sleep(1)
        return get_drive()

def calibrate(odrv):
    odrv.axis0.requested_state = odrive.enums.AxisState.FULL_CALIBRATION_SEQUENCE
    while odrv.axis0.current_state != odrive.enums.AxisState.IDLE:
        time.sleep(0.1)

def app_reboot(odrv):
    try:
        odrv.reboot()
    finally:
        return get_drive()


if __name__ == 'main':
    drv = get_drive()
    set_config(drv)
    drv = save_to_nvm(drv)