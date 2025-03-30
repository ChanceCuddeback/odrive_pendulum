from pint import UnitRegistry
import matplotlib.pyplot as plt
import numpy as np

from pendulum import Pendulum
from motor import Motor, MotorInput
from config import ureg
from utils import ewma

#TODO: Profile this for insanely slow portion

if __name__ == '__main__':

    # Initialize the motor
    motor = Motor()
    motor.start()
    m_input = MotorInput()

    # Initialize the pendulum
    l = 250 * ureg.millimeter
    m = 6 * ureg.gram
    x_0 = (np.pi/2) * ureg.rad
    xdot_0 = 0 * ureg.angular_velocity
    b = 0.0002 * ureg.damping
    delta_t = 2 * ureg.millisecond
    T = 25 * ureg.second

    pendulum = Pendulum(length=l, mass=m, theta0=x_0, omega0=xdot_0, damping=b, dt=delta_t)

    # Simulation parameters
    num_steps = int((T / delta_t).to_base_units().magnitude)
    time_values = []
    angle_values = []
    angular_velocity_values = []

    print("Starting simulation...")
    print(f"{'Time (s)':>10} {'Angle (rad)':>12} {'Angular Velocity (rad/s)':>20}")

    old_torque = 0
    for step in range(num_steps):
        # Current time
        current_time = step * delta_t.to_base_units().magnitude

        # Get the current state of the pendulum
        theta, omega = pendulum.get_state()

        # Step the pendulum simulation
        accel = pendulum.step(0 * ureg.newton_meter)

        m_input.tDes = ewma(accel.to_base_units().magnitude, old_torque, 0.001)
        motor.run(m_input)
        old_torque = m_input.tDes

        # Log the state
        time_values.append(current_time)
        angle_values.append(theta)
        angular_velocity_values.append(omega)

        # Print the state
        print(f"{current_time:10.4f} {theta:12.4f} {omega:20.4f}")

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