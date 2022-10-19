#!/usr/bin/env python3

from lib2to3.pgen2.token import NOTEQUAL
import numpy as np

# =====================================================================
# GLobal Variables
# =====================================================================

# LRV vehicle characteris
b = 0.229       # wheel width (m)
D = 0.813        # wheel diameter (m)
m = 672         # vehicle mass (kg)
num = 4         # number of wheels


# soil characteristics, Lunar Regolith
c_m = 170         # cohesive strength of soil (N/m^2)
c_cm = 0.017      # cohesive strength of soil (N/cm^2)
cf = 0.05        # friction co.efficient
rho = 1600       # soil density (kg/m^3)
gamma = 2470    # weight density of soil (N/m^3)
g_moon = 1.541   # gravitational acc on moon (m/s^2) 

k_c = 1400             # modulus of cohesion of soil deformation (N/m^2)
k_phi =  830000        # modulus of friction of soil deformation (N/m^3)


phi = 33        # angle of internal resistance of soil? (deg)
theta = 15      # slope angle for gravitational resistance (deg)
n = 1           # constant 1

# Additional Variables
W = g_moon * m       # weight of vehivle on moon
W_wh = W / num       # weight on each wheel
print(W)
# =====================================================================
# Helper Functions
# =====================================================================

# assuming n = 1
def compression_resitance(k_c, k_phi, b, W_wh, D):
    kbk = k_c + b * k_phi 
    z = ((3 * W_wh / (2 * kbk * np.sqrt(D))))**(2/3)
    R_c = (1/2) * (kbk ** (-1/3)) * (3 * W_wh / (2 * np.sqrt(D)))**(4/3)
    return(z, R_c)

def bulldozing_resitance(b, alpha, phi, z, c_m, K_c, gamma, K_phi, l_o):
    part1 =
    part2 =
    part3 =
    return()

def rolling_resitance(W,cf):
    R_r = W*cf
    return(R_r)

def gravitational_resitance(W, theta):
    R_g = W * np.sin(np.radians(theta))
    return(R_g)

def modulus_soil_deformation(Nc, Ng, phi):
    cos_sq_phi = (np.cos(phi))**2
    K_c = (Nc - np.tan(phi)) * cos_sq_phi
    K_phi = (1 + (2 * Ng / np.tan(phi)))
    return(K_c, K_phi)

def angle_of_approach(z, D):
    alpha = np.arccos(1 - (2*z/D))
    return(alpha)

def length_of_soil_ruptured(z, phi):
    l_o =z * np.tan((np.pi/4) - (np.radians(phi)/2))
    return(l_o)

# =====================================================================
# Terzaghi Analysis of Soil Deformation
# =====================================================================

def terzaghi(phi):
    phi = np.radians(phi)
    N_q = np.exp(np.tan(phi) * ((np.pi*3/2)-phi)) / (2 * (np.cos((np.pi/4)+phi/2))**2)
    N_c = (N_q - 1) / np.tan(phi)
    N_g = 2 * (N_q+1) * np.tan(phi) / (1 + 0.4 * np.sin(4 * phi))
    return(N_q, N_c, N_g)


# =====================================================================
# Bulldozing 
# =====================================================================



# Main Function
def main():
    z, R_c = compression_resitance(k_c, k_phi, b, W_wh, D)
    R_r = rolling_resitance(W, cf)
    R_g = gravitational_resitance(W, theta)
    N_q, N_c, N_g = terzaghi(phi)
    alpha = angle_of_approach(z, D)
    l_o = length_of_soil_ruptured(z, phi)
    K_c, K_phi = modulus_soil_deformation(N_c, N_g, phi)
    R_b = bulldozing_resitance(b, alpha, phi, z, c_m, K_c, gamma, K_phi, l_o)
    
    # print all results
    print("==================================================================")
    print("Compression Depth ==>", np.round(z,4), ' m')
    print("Compression Resistance ==>", np.round(R_c,4), ' N')
    print("==================================================================")
    print("Rolling Resistance ==>", np.round(R_r,4), ' N')
    print("Gravitational Resistance ==>", np.round(R_g,4), ' N')
    print("==================================================================")
    print("N_q ==>", np.round(N_q,4), '||  N_c ==>', np.round(N_c,4),'||  N_g ==>', np.round(N_g,4))
    print("==================================================================")


if __name__ == "__main__":
    main()