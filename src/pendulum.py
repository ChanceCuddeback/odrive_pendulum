from pint import UnitRegistry
import numpy as np

from config import ureg

class Pendulum:
    @ureg.wraps(None, (None, ureg.meter, ureg.kilogram, ureg.radian, ureg.angular_velocity, ureg.acceleration, ureg.second))
    def __init__(self, length=1*ureg.meter, mass=1*ureg.kilogram, theta0=1*ureg.radian, 
                 omega0=1*ureg.angular_velocity, g=9.81*ureg.acceleration, dt=0.01*ureg.second):
        self.length = length
        self.mass = mass
        self.theta = theta0
        self.omega = omega0
        self.g = g
        self.dt = dt
    
    @ureg.wraps(None, (None, ureg.newton_meter))
    def step(self, u):
        """
        Perform one time step of the simulation using the Euler method.
        """
        # Calculate angular acceleration
        alpha = (-(self.g / self.length) * np.sin(self.theta)) + u / (self.mass * self.length**2)
        
        # Update angular velocity and angular displacement
        self.omega += alpha * self.dt
        self.theta += self.omega * self.dt

    def get_state(self):
        return self.theta, self.omega
