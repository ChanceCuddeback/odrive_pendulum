from pint import UnitRegistry
import matplotlib.pyplot as plt
import numpy as np
import time

from pendulum import Pendulum
from motor import Motor

if __name__ == '__main__':

    # Initialize the motor
    motor = Motor()
    motor.start()

    # Initialize the pendulum
    ureg = UnitRegistry()
    l = 100 * ureg.millimeter
    m = 3.92 * ureg.gram
    x_0 = 45 * ureg.rad
    xdot_0 = 0 * ureg.Hz
    delta_t = 2 * ureg.millisecond
    T = 25 * ureg.second

    pendulum = Pendulum(length=l, mass=m, theta0=x_0, omega0=xdot_0, dt=delta_t)

    # Simulation parameters
    num_steps = int((T / delta_t).to_base_units().magnitude)
    time_values = []
    angle_values = []
    angular_velocity_values = []

    print("Starting simulation...")
    print(f"{'Time (s)':>10} {'Angle (rad)':>12} {'Angular Velocity (rad/s)':>20}")

    for step in range(num_steps):
        # Current time
        current_time = step * delta_t.to_base_units().magnitude

        # Get the current state of the pendulum
        theta, omega = pendulum.get_state()

        # Apply a control torque (e.g., proportional control to stabilize at 0 rad)
        desired_angle = 0 * ureg.rad
        error = (desired_angle - theta).to_base_units().magnitude
        torque = -0.1 * error * ureg.newton_meter  # Proportional control

        # Set the torque on the motor
        motor.set_torque(torque.to_base_units().magnitude)

        # Step the pendulum simulation
        pendulum.step(torque)

        # Log the state
        time_values.append(current_time)
        angle_values.append(theta.to_base_units().magnitude)
        angular_velocity_values.append(omega.to_base_units().magnitude)

        # Print the state
        print(f"{current_time:10.4f} {theta.to_base_units().magnitude:12.4f} {omega.to_base_units().magnitude:20.4f}")

    # Stop the motor
    motor.stop()

    print("Simulation complete.")

    # Plot the results
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.plot(time_values, angle_values, label="Angle (rad)")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (rad)")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time_values, angular_velocity_values, label="Angular Velocity (rad/s)", color="orange")
    plt.xlabel("Time (s)")
    plt.ylabel("Angular Velocity (rad/s)")
    plt.legend()

    plt.tight_layout()
    plt.show()