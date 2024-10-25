from pint import UnitRegistry
import numpy as np

class Pendulum:
    ureg = UnitRegistry()
    @ureg.wraps(None, [ureg.meter, ureg.gram, ureg.rad, ureg.Hz])
    def __init__(self, length, mass, theta0, omega0, g=9.81*ureg['meter/second**2'], dt=0.01*ureg['second']):
        self.length = length
        self.mass = mass
        self.theta = theta0
        self.omega = omega0
        self.g = g
        self.dt = dt
    
    def step(self, u):
        """
        Perform one time step of the simulation using the Euler method.
        """
        # Calculate angular acceleration
        alpha = (-(self.g / self.length) * np.sin(self.theta)) + u.to()
        
        # Update angular velocity and angular displacement
        self.omega += alpha * self.dt
        self.theta += self.omega * self.dt

    def get_state(self):
        return self.theta, self.omega

    def simulate(self, num_steps):
        trajectory = []
        for _ in range(num_steps):
            self.step()
            trajectory.append(self.get_state())
        return trajectory