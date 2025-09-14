import numpy as np  
import matplotlib.pyplot as plt
import scipy.integrate 

import wavefuncitons
from wavefuncitons import corenell_wave_function

from enum import Enum
from data import ParticleNames, quark_masses, quarkonium_masses

import numericalSolvers


def count_nodes_and_turns(u,v,r):
    node_count = 0
    turn_count = 0
    for i in range(len(r) -1):
        cross_up = u[i] <= 0 and u[i+1] >= 0
        cross_down = u[i] >= 0 and u[i+1] <= 0
        
        turn_up = v[i] >= 0 and v[i+1] <= 0
        turn_down = v[i] <= 0 and v[i+1] >= 0
        
        if cross_up or cross_down:
            node_count += 1
        if turn_up or turn_down:
            turn_count +=1
            
    return node_count, turn_count

U0 = [0,1]
alpha = 0.4
init_beta = 0.195

charm_quark_mass = 1.27
charmonium_mass_1S = 2.9839

# charmonium_energy_1S = charmonium_mass_1S - 2*charm_quark_mass
#mu = mc/2

recpricol_reduced_mass = 1/charm_quark_mass + 1/charm_quark_mass
reduced_mass = 1/recpricol_reduced_mass
r = np.linspace(0.0000001, 15, 10000)

charmonium_energy_1S = quarkonium_masses[ParticleNames.CHARMONIUM]['1S'] - 2*quark_masses[ParticleNames.CHARM]


# beta, sol = recursive_staircase_solver(U0, alpha, epsilon_lower=init_beta, fixed_value=charmonium_energy_1S, layer=30)
beta, sol = numericalSolvers.recursive_staircase_solver(U0, r, corenell_wave_function, alpha, 
        charmonium_energy_1S, reduced_mass= reduced_mass ,epsilon_lower = init_beta, calibration_mode = True, flight = 30)

u = sol[:,0]
pdf = wavefuncitons.square_wavefunction(u)

print(beta)
plt.plot(r, pdf)
plt.show()


