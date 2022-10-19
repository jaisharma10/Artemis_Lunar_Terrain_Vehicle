#!/usr/bin/env python3

# =====================================================================
# GLobal Variables
# =====================================================================

# LRV vehicle characteris
b = 0.24        # wheel width (m)
D = 0.81        # wheel diameter (m)
m = 640         # vehicle mass (kg)
num = 4         # number of wheels


# soil characteristics
c1 = 170         # cohesive strength of soil (N/m^2)
c2 = 0.017       # cohesive strength of soil (N/cm^2)
cf = 0.05        # friction co.efficient
rho1 = 1600       # soil density (kg/m^3)
rho2 = 2470       # soil density (N/m^3)
g_moon = 1.625  # gravitational acc on moon (m/s^2) 


phi = 33        # slope (deg)
n = 1           # constant 1

# Additional Variables
w = g_moon * m       # weight of vehivle on moon
w_wh = w / num       # weight on each wheel


# =====================================================================
# Helper Functions
# =====================================================================

def compression_resitance():
    return()

def bulldozing_resitance():
    return()


# =====================================================================
# Terzaghi Analysis of Soil Deformation
# =====================================================================

def terzaghi():
    return()


# =====================================================================
# Bulldozing 
# =====================================================================



# Main Function
def main():
    print("Hello World!")

if __name__ == "__main__":
    main()