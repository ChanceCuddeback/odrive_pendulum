from pint import UnitRegistry
import matplotlib.pyplot as plt
import numpy as np
import time

from pendulum import *
from motor import *


if __name__ == '__main__':
    # initialize pendulum
    ureg = UnitRegistry()
    l = 100 * ureg.millimeter
    m = 3.92 * ureg.gram
    x_0 = 45 * ureg.rad
    xdot_0 = 0 * ureg.Hz
    delta_t = 2 * ureg.millisecond
    T = 25 * ureg.second
    

    x = np.array([])
    xdot = np.array([])
    t0 = time.monotonic()
    
    