import numpy as np

class Pendulum:
    def __init__(self, length, mass, theta0, omega0, g=9.81, dt=0.01):
        self.length = length
        self.mass = mass
        self.theta = theta0  # Angular displacement (radians)
        self.omega = omega0  # Angular velocity (rad/s)
        self.g = g  # Gravitational acceleration (m/s^2)
        self.dt = dt  # Time step for simulation (s)
    
    def step(self, u):
        """
        Perform one time step of the simulation using the Euler method.
        """
        # Calculate angular acceleration
        alpha = (-(self.g / self.length) * np.sin(self.theta)) + u
        
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