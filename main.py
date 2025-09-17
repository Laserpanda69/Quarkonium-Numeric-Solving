import numpy as np  
import matplotlib.pyplot as plt
import scipy.integrate 

import wavefuncitons as wfns

from enum import Enum
from data import ParticleNames, particle_masses, physical_constants

import numericalSolvers as Solvers



U0 = [0,1]
WAVE_FUNCTION = wfns.corenell_wave_function
N = 1


ALPHA_S = physical_constants['strong_coupling_constant']


initial_charmonium_cornell_beta = 0.195

CHARM_QUARK_MASS = particle_masses[ParticleNames.CHARM]
CHARMONIUM_1S_MASS = particle_masses[ParticleNames.CHARMONIUM]['experimental']['1S']


recpricol_reduced_mass = 1/CHARM_QUARK_MASS + 1/CHARM_QUARK_MASS
CHARMONIUM_REDUCED_MASS = 1/recpricol_reduced_mass
r = np.linspace(0.0000001, 15, 1000)

charmonium_1S_energy = CHARMONIUM_1S_MASS - 2*particle_masses[ParticleNames.CHARM]


# beta, sol = recursive_staircase_solver(U0, alpha, epsilon_lower=init_beta, fixed_value=charmonium_energy_1S, layer=30)

wavefunction_arguments = (initial_charmonium_cornell_beta,
    CHARMONIUM_REDUCED_MASS, charmonium_1S_energy)

# calibration staircase will handover l = 0 automatically to wavefunction so
# l doesn't need to be a potential argument
calibrated_variable, sol = Solvers.calibration_staircase(
        U0, r, WAVE_FUNCTION , 
        potential_arguments=(charmonium_1S_energy, CHARMONIUM_REDUCED_MASS),
        b_lower = initial_charmonium_cornell_beta, 
        flight = 30
    )

print(calibrated_variable)

u = sol[:,0]
v = sol[:,1]

pdf = wfns.square_wavefunction(u)
pdf, u, v = wfns.normalise_wavefunction(pdf, u, v, r)
plt.plot(r, pdf, color = 'red', linestyle =  'dashed')

plt.plot(r, [0]*r, color = "lightgrey", linestyle='dashed')
# print(f"charmonium_energy_1S = {charmonium_1S_energy}")

line_styles = ['solid', 'dotted', 'dashdot']

last_energy_value = 0
offset = 0

line_styles = ['dotted', 'dashdot', 'dashed']

for n in range(N+1):
    for l in range(0, n):
        E, sol = Solvers.solve_for_energy(
            U0, r, WAVE_FUNCTION , n,
            potential_arguments=(l, calibrated_variable, CHARMONIUM_REDUCED_MASS),
            epsilon_lower = last_energy_value + offset, 
            flight = 30
        )
        u = sol[:,0]
        v= sol[:,1]
                
        
        pdf = wfns.square_wavefunction(u)
        pdf, u, v = wfns.normalise_wavefunction(pdf, u, v, r)
        
        # ls = 'solid' if n == 1 else line_styles[l%len(line_styles)]
        ls = line_styles[l%len(line_styles)]
        plt.plot(r, pdf, linestyle = ls)
        # print(f"E_{n}{l} = {E}")
        print(f"M_{n}{l} = {E+2*CHARM_QUARK_MASS}")
        last_energy_value = E

# for i in range(len(wfns)-1):
#     print(np.array_equal(wfns[i], wfns[i+1]))

# print(charmonium_beta)
plt.show()




