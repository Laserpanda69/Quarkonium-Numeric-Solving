import numpy as np  
import matplotlib.pyplot as plt
import scipy.integrate 

import wavefuncitons
from wavefuncitons import corenell_wave_function

from enum import Enum
from data import ParticleNames, particle_masses

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
charmonium_cornell_alpha = 0.4
initial_charmonium_cornell_beta = 0.195

charm_quark_mass = particle_masses[ParticleNames.CHARM]
charmonium_mass_1S = particle_masses[ParticleNames.CHARMONIUM]['1S']


recpricol_reduced_mass = 1/charm_quark_mass + 1/charm_quark_mass
reduced_charmonium_mass = 1/recpricol_reduced_mass
r = np.linspace(0.0000001, 15, 10000)

charmonium_energy_1S = particle_masses[ParticleNames.CHARMONIUM]['1S'] - 2*particle_masses[ParticleNames.CHARM]


# beta, sol = recursive_staircase_solver(U0, alpha, epsilon_lower=init_beta, fixed_value=charmonium_energy_1S, layer=30)

wavefunction_arguments = (charmonium_cornell_alpha, initial_charmonium_cornell_beta,
    reduced_charmonium_mass, charmonium_energy_1S)

charmonium_beta, sol = numericalSolvers.calibration_staircase(
        U0, r, corenell_wave_function, 
        potential_arguments=(charmonium_cornell_alpha, charmonium_energy_1S, reduced_charmonium_mass),
        b_lower = initial_charmonium_cornell_beta, 
        flight = 30
    )

# u = sol[:,0]
# pdf = wavefuncitons.square_wavefunction(u)
# plt.plot(r, pdf)

last_energy_value = charmonium_energy_1S - 0.1
offset = 0.01
print(f"charmonium_energy_1S = {charmonium_energy_1S}")
N = 5
for n in range(N + 1):
    for l in range(0, n):
        E, sol = numericalSolvers.erergy_staircase(
            U0, r, corenell_wave_function, 
            potential_arguments=(l, charmonium_cornell_alpha, charmonium_beta, reduced_charmonium_mass),
            epsilon_lower = last_energy_value + offset, 
            flight = 20
        )
        
        u = sol[:,0]
        pdf = wavefuncitons.square_wavefunction(u)
        plt.plot(r, pdf)
        print(f"E_{n}{l} = {E}")
        last_energy_value = E

print(charmonium_beta)
plt.show()


