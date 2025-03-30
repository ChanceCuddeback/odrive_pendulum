from src.pendulum import Pendulum
from pint import UnitRegistry
import numpy as np

from src.config import ureg

def test_pendulum_initialization():
    length = 1 * ureg.meter
    mass = 1 * ureg.kilogram
    theta0 = 0.1 * ureg.radian
    omega0 = 0 * ureg.angular_velocity
    pendulum = Pendulum(length, mass, theta0, omega0)

    print(ureg.default_system)

    assert pendulum.length == length.to_base_units().magnitude
    assert pendulum.mass == mass.to_base_units().magnitude
    assert pendulum.theta == theta0.to_base_units().magnitude
    assert pendulum.omega == omega0.to_base_units().magnitude

def test_pendulum_step():
    length = 1 * ureg.meter
    mass = 1 * ureg.kilogram
    theta0 = 0.1 * ureg.radian
    omega0 = 0 * ureg.angular_velocity
    dt = 0.01 * ureg.second
    pendulum = Pendulum(length, mass, theta0, omega0, dt=dt)

    torque = 0 * ureg.newton_meter
    pendulum.step(torque)

    # Check that the state has been updated
    assert pendulum.theta != theta0.to_base_units().magnitude
    assert pendulum.omega != omega0.to_base_units().magnitude
