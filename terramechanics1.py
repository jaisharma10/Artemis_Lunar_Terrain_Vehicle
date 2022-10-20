#!/usr/bin/env python3

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
W = g_moon * m       # weight of vehicle on moon
W_wh = W / num       # weight on each wheel

# Grousers
num_gr = 16          # number of grousers
r = D/2              # radius of grouser
h = 0.05             # height of grouser (m)

# more constants
# s = 0.035      # wheel slip ratio 
s = 0.5
K = 0.018      # shear deformation modulus (m)


# =====================================================================
# Resistances
# =====================================================================

def compression_resitance(k_c, k_phi, b, W_wh, D):
    # assuming n = 1
    kbk = k_c + b * k_phi 
    z = ((3 * W_wh / (2 * kbk * np.sqrt(D))))**(2/3)
    R_c = (1/2) * (kbk ** (-1/3)) * (3 * W_wh / (2 * np.sqrt(D)))**(4/3)
    return(z, R_c)

def bulldozing_resitance(b, alpha, phi, z, c_m, K_c, gamma, K_phi, l_o):
    phi = np.radians(phi)
    # alpha and phi are in radians now
    part1 = (b * np.sin(alpha+phi)) * ((2*z*c_m*K_c) + (gamma*(z**2)*K_phi)) / (2 * np.sin(alpha) * np.cos(phi))
    part2 = ((l_o**3)*gamma/3 * (np.pi/2 - phi))
    part3 = c_m*(l_o**2)*(1 + np.tan(np.pi/4  + phi/2))
    R_b = part1 + part2 + part3
    # print("part1 ==>", np.round(part1,6), '||  part2 ==>', np.round(part2,6),'||  part3 ==>', np.round(part3,6))

    return(R_b)

def rolling_resitance(W,cf):
    R_r = W*cf
    return(R_r)

def gravitational_resitance(W, theta):
    R_g = W * np.sin(np.radians(theta))
    return(R_g)

# =====================================================================
# Tractive Forces
# =====================================================================

def grousers_params(num_gr, r, l):
    # num_gr = N in lecture notes
    psi = 2 * np.pi / num_gr        # angle between grousers
    l_g = psi * r                   # distance between grousers
    N_g = l_g / l                   # number of grousrs in ground contact
    return(N_g)

def tractiveForce_NoGrousers(b,l,c_m,h, N_g):
    return()

def tractiveForce_Grousers(l, N_g):
    phi = np.radians(35) # soil angle of internal friction (rad)
    part1 = b * l * c_m * N_g * (1 + 2*h/b)
    part2 = W * np.tan(phi) * (1 + (0.64*h/b) * np.arctan(b/h))
    part3 = 1 - (K / (s*l) * (1 - np.exp( -s * l / K)))
    H = (part1 + part2) * part3
    # print("tractiveForce_Grousers ==>", H)
    return(H)

# =====================================================================
# Drawbar Pull
# =====================================================================

def drawbarPull(H, R_c_total, R_r, R_g, R_b_total):
    R_total = R_c_total + R_r + R_g +R_b_total
    DP = H - R_total
    return(DP)

# =====================================================================
# Helper Functions
# =====================================================================

def modulus_soil_deformation(Nc, Ng, phi):
    phi = np.radians(phi)         # convert to radians
    cos_sq_phi = (np.cos(phi))**2
    K_c = (Nc - np.tan(phi)) * cos_sq_phi
    K_phi = (1 + (2 * Ng / np.tan(phi)))
    return(K_c, K_phi)

def angle_of_approach(z, D):
    alpha = np.arccos(1 - (2*z/D))  # output in radians
    return(alpha)

def length_of_soil_ruptured(z, phi):
    l_o =z * np.tan((np.pi/4) - (np.radians(phi)/2))
    return(l_o)

def length_of_contact_patch(z,D):
    l = (D/2) * np.arccos(1 - (2*z/D))
    return(l)

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
# Main Function
# =====================================================================

def main():
    
    # compute resistances
    z, R_c = compression_resitance(k_c, k_phi, b, W_wh, D)      # compression resistance on one wheel
    
    # get rquired variables
    N_q, N_c, N_g = terzaghi(phi)
    alpha = angle_of_approach(z, D)
    l = length_of_contact_patch(z,D)
    l_o = length_of_soil_ruptured(z, phi)
    K_c, K_phi = modulus_soil_deformation(N_c, N_g, phi)
    
    R_c_total = R_c * num                                       # total compression resistance on vehicle
    R_r = rolling_resitance(W, cf)
    R_g = gravitational_resitance(W, theta)
    R_b = bulldozing_resitance(b, alpha, phi, z, c_m, K_c, gamma, K_phi, l_o)  
    R_b_total = 2 * R_b      # total bulldozing resistance for the two front wheels
    
    # print all results
    print("==================================================================")
    print("Compression Depth ==>", np.round(z,4), ' m')
    print("Compression Resistance ==>", np.round(R_c_total,4), ' N')
    print("==================================================================")
    print("Rolling Resistance ==>", np.round(R_r,4), ' N')
    print("Gravitational Resistance ==>", np.round(R_g,4), ' N')
    print("Bulldozing Resistance ==>", np.round(R_b_total,4), ' N')
    print("==================================================================")
    print("K_c ==>", np.round(K_c,4), '||  K_phi ==>', np.round(K_phi,4))
    print("N_q ==>", np.round(N_q,4), '||  N_c ==>', np.round(N_c,4),'||  N_g ==>', np.round(N_g,4))
    print("==================================================================")

    # total Resistance on flat ground
    R_tot_flat = R_c_total + R_r + R_b_total
    # total Resistance on incline (theta --> 15 degrees)
    R_tot_slope = R_c_total + R_r + R_b_total + R_g
    print("Total Resistance, flat ground ==>", np.round(R_tot_flat,4), ' N')
    print("Total Resistance, 15 deg slope ==>", np.round(R_tot_slope,4), ' N')
    print("==================================================================")
    
    s_list = [1,2,3]
    for s in s_list:
        print(s)
    
    # grouser study
    N_g = grousers_params(num_gr, r, l)
    H = tractiveForce_Grousers(l, N_g)
    print("Number of Grousrs in ground contact ==>", np.round(N_g,0))
    print("Maximum Tractive Force of Wheels ==>", np.round(H, 4))
    
    print("==================================================================")
    
    # compute Draw Bar pull 
    DP = drawbarPull(H, R_c_total, R_r, R_g, R_b_total)
    print("Drawbar Pull (residual drive force) ==>", np.round(DP, 4))
    print("==================================================================")


if __name__ == "__main__":
    main()