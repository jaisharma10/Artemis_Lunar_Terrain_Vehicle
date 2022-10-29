# Stability Calculation
import imp
from math import radians, sqrt
from math import cos
from math import sin
from math import atan
from math import degrees
from math import radians
import matplotlib.pyplot as plt
import numpy as np


"""
V: vehivle velocity (m/s)
a: CM offset from wheel1 (m)
l: distance from front to rear wheel (m)
h: CM height from level of wheel center (m)
r: wheel radius (m)
m: vehicle mas (kg)
g: gravity (m/s2)

"""

def normal_1(m, g, a, l, h, r, theta_deg, ax):
    theta_rad = radians(theta_deg)
    N1 = m*g*((1-(a/l))*cos(theta_rad)-((h+r)/l)*sin(theta_rad)-(ax/g))
    return N1

def normal_2(m, g, a, l, h, r, theta_deg, ax):
    theta_rad = radians(theta_deg)
    N2 = m*g*((a/l)*cos(theta_rad)+((h+r)/l)*sin(theta_rad)+(ax/g))
    return N2

def thrust_1(m, g, a, l, h, r, theta_deg, ax):
    theta_rad = radians(theta_deg)
    N1 = normal_1(m, g, a, l, h, r, theta_rad, ax)
    N2 = normal_2(m, g, a, l, h, r, theta_rad, ax)
    T1 = (m*g*sin(theta_rad)+m*ax)*N1/(N1+N2)
    return T1

def thrust_2(m, g, a, l, h, r, theta_deg, ax):
    theta_rad = radians(theta_deg)
    N1 = normal_1(m, g, a, l, h, r, theta_rad, ax)
    N2 = normal_2(m, g, a, l, h, r, theta_rad, ax)
    T2 = (m*g*sin(theta_rad)+m*ax)*N2/(N1+N2)
    return T2

def tipping_angle(a, l, h, r):
    tipping_ang_rad = atan((1-(a/l))/((h+r)/l))
    tipping_ang_deg = degrees(tipping_ang_rad)
    return tipping_ang_deg

def tipping_ax(g, a, h, r, theta_deg):
    theta_rad = radians(theta_deg)
    ax_lim = g*((a/(h+r))*cos(theta_rad)-sin(theta_rad))
    return ax_lim

def tipping_turning_radius(g, y, h, V, theta_deg):
    theta_rad = radians(theta_deg)
    r_lim = ((V**2)/g)*(1/((y/h)*cos(theta_rad)-sin(theta_rad)))
    return r_lim

# Parameters
r = 0.4
h = 0.5
V = 4.0
sample = 100
g = 1.62 
l = np.linspace(1, 3, num=sample)

# Initialize tipping angle variable
tipping_ang = np.zeros(sample)
tipping_acc_0 = np.zeros(sample)
tipping_acc_10 = np.zeros(sample)
tipping_acc_20 = np.zeros(sample)
tipping_acc_30 = np.zeros(sample)
tipping_radius_0 = np.zeros(sample)
tipping_radius_10 = np.zeros(sample)
tipping_radius_20 = np.zeros(sample)
tipping_radius_30 = np.zeros(sample)

for i in range(sample):
    tipping_ang[i] = tipping_angle(l[i]/2, l[i], h, r)
    tipping_acc_0[i] = tipping_ax(g, l[i]/2, h, r, 0)
    tipping_acc_10[i] = tipping_ax(g, l[i]/2, h, r, 10)
    tipping_acc_20[i] = tipping_ax(g, l[i]/2, h, r, 20)
    tipping_acc_30[i] = tipping_ax(g, l[i]/2, h, r, 30)
    tipping_radius_0[i] = tipping_turning_radius(g, l[i]/2, h, V, 0)
    tipping_radius_10[i] = tipping_turning_radius(g, l[i]/2, h, V, 10)
    tipping_radius_20[i] = tipping_turning_radius(g, l[i]/2, h, V, 20)
    tipping_radius_30[i] = tipping_turning_radius(g, l[i]/2, h, V, 30)

plt.figure()
plt.plot(l, tipping_ang, 'b-')
plt.title("Stability on Slope")
plt.xlabel("Vehicle Width (m)")
plt.ylabel("Tipping Angle (deg)")
plt.grid(linestyle = '--', linewidth = 0.5)

plt.figure()
plt.plot(l, tipping_acc_0, 'r-',  label="0 deg")
plt.plot(l, tipping_acc_10, 'g-',  label="10 deg")
plt.plot(l, tipping_acc_20, 'b-',  label="20 deg")
plt.plot(l, tipping_acc_30, 'y-',  label="30 deg")
plt.title("Stability under Acceleration")
plt.xlabel("Vehicle Length (m)")
plt.ylabel("Tipping Acceleration (m/s2)")
plt.legend(loc="lower right")
plt.grid(linestyle = '--', linewidth = 0.5)

plt.figure()
plt.plot(l, tipping_radius_0, 'r-',  label="0 deg")
plt.plot(l, tipping_radius_10, 'g-',  label="10 deg")
plt.plot(l, tipping_radius_20, 'b-',  label="20 deg")
plt.plot(l, tipping_radius_30, 'y-',  label="30 deg")
plt.title("Turning Stability on Slope")
plt.xlabel("Vehicle Width (m)")
plt.ylabel("Tipping Turning Radius (m)")
plt.legend(loc="upper right")
plt.grid(linestyle = '--', linewidth = 0.5)
plt.show()