import numpy as np  
import matplotlib.pyplot as plt
import scipy.integrate 

import wavefuncitons
from wavefuncitons import corenell_wave_function

from enum import Enum
from data import ParticleNames, particle_masses

import numericalSolvers



U0 = [0,1]
charmonium_cornell_alpha = 0.4
initial_charmonium_cornell_beta = 0.195

charm_quark_mass = particle_masses[ParticleNames.CHARM]
charmonium_mass_1S = particle_masses[ParticleNames.CHARMONIUM]['1S']


recpricol_reduced_mass = 1/charm_quark_mass + 1/charm_quark_mass
reduced_charmonium_mass = 1/recpricol_reduced_mass
r = np.linspace(0.0000001, 15, 1000)

charmonium_energy_1S = particle_masses[ParticleNames.CHARMONIUM]['1S'] - 2*particle_masses[ParticleNames.CHARM]


# beta, sol = recursive_staircase_solver(U0, alpha, epsilon_lower=init_beta, fixed_value=charmonium_energy_1S, layer=30)

wavefunction_arguments = (initial_charmonium_cornell_beta,
    reduced_charmonium_mass, charmonium_energy_1S)

print("Calibrating")
charmonium_beta, sol = numericalSolvers.calibration_staircase(
        U0, r, corenell_wave_function, 
        potential_arguments=(charmonium_energy_1S, reduced_charmonium_mass),
        b_lower = initial_charmonium_cornell_beta, 
        flight = 30
    )

u = sol[:,0]
pdf = wavefuncitons.square_wavefunction(u)
plt.plot(r, pdf)

last_energy_value = charmonium_energy_1S - 0.1
offset = 0.01
print(f"charmonium_energy_1S = {charmonium_energy_1S}")
N = 3

line_styles = ['dotted', 'dashdot', 'dashed']

print("Solving")
wfns = []
for n in [1, 2, 3, 4, 5, 6]:
    for l in range(0, n):
        E, sol = numericalSolvers.solve_for_energy(
            U0, r, corenell_wave_function, n,
            potential_arguments=(l, charmonium_beta, reduced_charmonium_mass),
            epsilon_lower = last_energy_value + offset, 
            flight = 30
        )
        u = sol[:,0]
        v= sol[:,1]
                
        pdf = wavefuncitons.square_wavefunction(u)
        pdf, u, v = wavefuncitons.normalise_wavefunction(r, pdf, u, v)
        # if max(pdf) > 2:
        #     print(f"{n}{l} has a PDF with a peak amplitude of {max(pdf)}")
        #     continue
        
        plt.plot(r, pdf, linestyle = line_styles[l%len(line_styles)])
        print(f"E_{n}{l} = {E}")
        # print(f"M_{n}{l} = {E+2*charm_quark_mass}")
        last_energy_value = E

# for i in range(len(wfns)-1):
#     print(np.array_equal(wfns[i], wfns[i+1]))

print(charmonium_beta)
plt.show()


