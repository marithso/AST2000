import numpy as np
import matplotlib.pyplot as plt

from ast2000tools.space_mission import SpaceMission
import ast2000tools.utils as utils
from ast2000tools.constants import *
from ast2000tools.solar_system import SolarSystem

#utils.check_for_newer_version()
# Construct SpaceMission instance for my mission
seed = utils.get_seed('Sgfrette')
mission = SpaceMission(seed)
system = SolarSystem(seed)
"""
This is the code for c2
"""
"""
Defined through looking at the generated plot
"""
L = 5
sigma = 0.001/5
sigma_P = 45/5
sigma_t0 = 25/5
max_val_v = 0.015+sigma
min_val_v = 0.0007-sigma
max_val_P = 60+sigma_P
min_val_P = 35-sigma_P
max_val_t0 = 10+sigma_t0
min_val_t0 = 5-sigma_t0

"""
Randomly given velocity to system
"""
val_of_cm = 46


infile = open("radial_velocity_data.txt", "r")
infile.readline()

time = []
vel = []
for line in infile:
    word = line.split()
    time.append(float(word[0]))
    vel.append(float(word[1]))


time = np.asarray(time)
vel_imp = np.asarray(vel)

"""
Implementing the quadratic method
"""

def minste_kvadrat(P,v_star, t_0, vel_imp):
    value = 0
    for i in range(len(time)):
        a = (vel_imp[i]-v_star*np.cos((2*np.pi/P)*(time[i]-t_0)))**2
        value += a
    return P,v_star, t_0,value


d_value_P = (max_val_P-min_val_P)/(L-1)
d_value_v = (max_val_v-min_val_v)/(L-1)
d_value_t0 = (max_val_v-min_val_v)/(L-1)
"""
Generating the different parameters we are going to check.
"""
P_values = np.asarray([min_val_P + d_value_P*i for i in range(L)])
v_star_values = np.asarray([min_val_v + d_value_v*i for i in range(L)])
t_0_values = np.asarray([min_val_t0 + d_value_t0*i for i in range(L)])

minste_kvadrat_liste = []
"""
Finding the set of parameters with smallest error
"""
for n in range(len(P_values+1)):
    for g in range(len(P_values+1)):
        for j in range(len(P_values+1)):
            b = minste_kvadrat(P_values[n],v_star_values[g],t_0_values[j],vel_imp)
            minste_kvadrat_liste.append(b)

minste_kvadrat_liste = np.asarray(minste_kvadrat_liste)
"""
Getting the parameters from the set with the smallest error.
"""
for i in range(len(minste_kvadrat_liste)):
    if minste_kvadrat_liste[i,3] == min(minste_kvadrat_liste[:,3]):
        index = np.where(minste_kvadrat_liste[i,3])


print(minste_kvadrat_liste[index[0]])
P,v_star,t_0,value =minste_kvadrat_liste[index[0]][0]

def V(t):
    return v_star*np.cos((2*np.pi*(t-t_0)/P))

plt.plot(time,vel_imp,label="Data")
plt.plot(time,V(time),label="Estimated curve")
plt.plot()

plt.xlabel("Years")
plt.ylabel("AU/Years")
plt.legend()
plt.savefig("read-vals-vetle.jpeg")
plt.show()
