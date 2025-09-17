import numpy as np  
import matplotlib.pyplot as plt
import scipy.integrate 

import wavefuncitons as wfns

from enum import Enum
from data import ParticleNames, PARTICLE_MASSES, PHYSICAL_CONSTANTS

import numericalSolvers as Solvers



U0 = [0,1]
ALPHA_S = PHYSICAL_CONSTANTS['strong_coupling_constant']



CHARM_QUARK_MASS = PARTICLE_MASSES[ParticleNames.CHARM]
CHARMONIUM_1S_MASS = PARTICLE_MASSES[ParticleNames.CHARMONIUM]['experimental']['1S']
recpricol_reduced_mass = 1/CHARM_QUARK_MASS + 1/CHARM_QUARK_MASS
CHARMONIUM_REDUCED_MASS = 1/recpricol_reduced_mass

CHARMONIUM_1S_ENERGY = CHARMONIUM_1S_MASS - 2*PARTICLE_MASSES[ParticleNames.CHARM]

# WAVE_FUNCTION = wfns.corenell_wave_function
WAVE_FUNCTION = wfns.bhanot_rudaz_wave_function
N = 1
F = 50
initial_idependent_variable = 0.01
wavefunction_arguments = None

if WAVE_FUNCTION == wfns.corenell_wave_function:
    # initial_idependent_variable = 0.195
    wavefunction_arguments = (CHARMONIUM_1S_ENERGY, CHARMONIUM_REDUCED_MASS)
elif WAVE_FUNCTION == wfns.bhanot_rudaz_wave_function:
    # initial_idependent_variable = 00.1
    wavefunction_arguments = (CHARMONIUM_1S_ENERGY, CHARMONIUM_REDUCED_MASS)


# beta, sol = recursive_staircase_solver(U0, alpha, epsilon_lower=init_beta, fixed_value=charmonium_energy_1S, layer=30)


# calibration staircase will handover l = 0 automatically to wavefunction so
# l doesn't need to be a potential argument
r_space = np.linspace(0.0000001, 15, 1000)
calibrated_variable, sol = Solvers.calibration_staircase(
        U0, r_space, WAVE_FUNCTION , 
        potential_arguments=wavefunction_arguments,
        b_lower = initial_idependent_variable, 
        flight = F
    )

print(calibrated_variable)

u = sol[:,0]
v = sol[:,1]

pdf = wfns.square_wavefunction(u)
pdf, u, v = wfns.normalise_wavefunction(pdf, u, v, r_space)
plt.plot(r_space, pdf, color = 'red', linestyle =  'dashed')

plt.plot(r_space, [0]*r_space, color = "lightgrey", linestyle='dashed')
# print(f"charmonium_energy_1S = {charmonium_1S_energy}")

line_styles = ['solid', 'dotted', 'dashdot']

last_energy_value = 0
offset = 0

line_styles = ['dotted', 'dashdot', 'dashed']

for n in range(N+1):
    for l in range(0, n):
        E, sol = Solvers.solve_for_energy(
            U0, r_space, WAVE_FUNCTION , n,
            potential_arguments=(l, *wavefunction_arguments),
            epsilon_lower = last_energy_value + offset, 
            flight = F
        )
        u = sol[:,0]
        v= sol[:,1]
                
        
        pdf = wfns.square_wavefunction(u)
        pdf, u, v = wfns.normalise_wavefunction(pdf, u, v, r_space)
        
        # ls = 'solid' if n == 1 else line_styles[l%len(line_styles)]
        ls = line_styles[l%len(line_styles)]
        plt.plot(r_space, pdf, linestyle = ls)
        # print(f"E_{n}{l} = {E}")
        print(f"M_{n}{l} = {E+2*CHARM_QUARK_MASS}")
        last_energy_value = E

# for i in range(len(wfns)-1):
#     print(np.array_equal(wfns[i], wfns[i+1]))

# print(charmonium_beta)
plt.show()




