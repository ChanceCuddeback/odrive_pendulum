from pint import UnitRegistry
import numpy as np

from config import ureg

class Pendulum:
    @ureg.wraps(None, (None, ureg.meter, ureg.kilogram, ureg.radian, ureg.angular_velocity, ureg.damping, ureg.acceleration, ureg.second))
    def __init__(self, length=1*ureg.meter, mass=1*ureg.kilogram, theta0=1*ureg.radian, 
                 omega0=1*ureg.angular_velocity, damping=0.0*ureg.damping, g=9.81*ureg.acceleration, dt=0.01*ureg.second):
        self.length = length
        self.mass = mass
        self.theta = theta0
        self.omega = omega0
        self.damping = damping
        self.g = g
        self.dt = dt
    
    @ureg.wraps(ureg.acceleration, (None, ureg.newton_meter))
    def step(self, u):
        """
        Perform one time step of the simulation using the Euler method.
        """
        # Calculate acceleration
        alpha = (((-1*self.mass*self.g*np.sin(self.theta)) - (self.damping*self.omega) + u))/(self.mass * self.length * self.length)
        
        # Update angular velocity and angular displacement
        self.omega += alpha * self.dt
        self.theta += self.omega * self.dt

        return alpha

    def get_state(self):
        return self.theta, self.omega
