# Steering Calculation
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

"""
V: vehivle velocity (m/s)
r: turning radius (m)
c: vehicle width (m)
l: vehicle length (l)
mu_r: rolling friction coefficient
mu_s: skid friction coefficient
N_o: outer wheel normal force (N)
N_ox: outer wheel normal force (x->f: front wheel, x->r: rear wheel) (N)
N_i: inner wheel normal force (N)
N_ix: inner wheel normal force (x->f: front wheel, x->r: rear wheel) (N)
"""

# Skid Steer
def skid_steer(V, r, c, l, mu_r, mu_s, N_o, N_i):
    P_ro = V*(1+(c/(2*r)))*mu_r*N_o # rolling power outer wheel (W)
    P_so = V*l*mu_s*N_o/(2*r) # skid power outer wheel (W)
    P_ri = V*(1-(c/(2*r)))*mu_r*N_i # rolling power inner wheel (W)
    P_si = V*l*mu_s*N_i/(2*r) # skid power outer wheel (W)
    P_total = 2*(P_ro + P_so + P_ri + P_si) # total power for 4 wheels (W)
    return P_total

# Diff Drive
def diff_drive(V, r, c, mu_r, N_o, N_i):
    P_ro = V*(1+(c/(2*r)))*mu_r*N_o # rolling power outer wheel (W)
    P_ri = V*(1-(c/(2*r)))*mu_r*N_i # rolling power inner wheel (W)
    P_total = P_ro + P_ri  # total power for 2 wheels (W)
    return P_total

# Single Akerman
def single_ackermann(V, r, c, l, mu_r, N_of, N_if, N_or, N_ir):
    P_rof = V*sqrt((1+(c/(2*r)))**2 + (l/r)**2)*mu_r*N_of
    P_rif = V*sqrt((1-(c/(2*r)))**2 + (l/r)**2)*mu_r*N_if
    P_wor = V*(1+(c/(2*r)))*mu_r*N_or
    P_wir = V*(1-(c/(2*r)))*mu_r*N_ir
    P_total = P_rof + P_rif + P_wor + P_wir # total power for 4 wheels (W)
    return P_total

# Double Akerman
def double_ackermann(V, r, c, l, mu_r, N_o, N_i):
    P_wo = V*sqrt((1+(c/(2*r)))**2 + (l/(2*r))**2)*mu_r*N_o
    P_wi = V*sqrt((1-(c/(2*r)))**2 + (l/(2*r))**2)*mu_r*N_i
    P_total = 2*(P_wo + P_wi) # total power for 4 wheels (W)
    return P_total

# Parameters
l = 2.286
c = 1.83
W = 1120
mu_r = 0.2
mu_s = 1
V = 4.0
sample = 100
r = np.linspace(2, 50, num=sample)

# Initialize power variables
P_skid = np.zeros(sample)
P_diff = np.zeros(sample)
P_single_acker = np.zeros(sample)
P_double_acker = np.zeros(sample)

for i in range(sample):
    P_skid[i] = skid_steer(V, r[i], c, l, mu_r, mu_s, W/4, W/4)
    P_diff[i] = diff_drive(V, r[i], c, mu_r, W/4, W/4)
    P_single_acker[i] = single_ackermann(V, r[i], c, l, mu_r, W/4, W/4, W/4, W/4)
    P_double_acker[i] = double_ackermann(V, r[i], c, l, mu_r, W/4, W/4)

plt.plot(r, P_skid, 'r-', label="Skid Steer")
plt.plot(r, P_diff, 'g-', label="Diff Drive")
plt.plot(r, P_single_acker, 'b-', label="Single Ackermann")
plt.plot(r, P_double_acker, 'y-', label="Double Ackermann")
plt.title("Steering Power Comparison")
plt.xlabel("Steering Radius (m)")
plt.ylabel("Steering Power (W)")
plt.legend(loc="upper right")
plt.grid(linestyle = '--', linewidth = 0.5)
plt.show()




