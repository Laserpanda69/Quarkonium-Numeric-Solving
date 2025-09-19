import numpy as np  
import matplotlib.pyplot as plt
import scipy.integrate 

import wavefuncitons
from wavefuncitons import corenell_wave_function

from enum import Enum
from data import ParticleNames, particle_masses

import numericalSolvers



U0 = [0,1]
initial_calibration_variable = 0.195

QUARK_MASS = particle_masses[ParticleNames.CHARM]
MESON_1S_MASS = particle_masses[ParticleNames.CHARMONIUM]['experimental']['1S']


recpricol_reduced_mass = 1/QUARK_MASS + 1/QUARK_MASS
REDUCED_MESON_MASS = 1/recpricol_reduced_mass
r = np.linspace(0.0000001, 15, 1000)

MESON_1S_ENERGY = particle_masses[ParticleNames.CHARMONIUM]['experimental']['1S'] - 2*particle_masses[ParticleNames.CHARM]


# beta, sol = recursive_staircase_solver(U0, alpha, epsilon_lower=init_beta, fixed_value=charmonium_energy_1S, layer=30)


print("Calibrating")
calibrated_variable, sol = numericalSolvers.calibration_staircase(
        U0, r, corenell_wave_function, 
        potential_arguments= (MESON_1S_ENERGY, REDUCED_MESON_MASS),
        b_lower = initial_calibration_variable, 
        flight = 30
    )

u, v= sol[:,0], sol[:,1]
pdf = wavefuncitons.square_wavefunction(u)
pdf, u, v = wavefuncitons.normalise_wavefunction(r, pdf, u, v)
plt.plot(r, pdf)

last_energy_value = MESON_1S_ENERGY - 0.1
offset = 0.01
print(f"charmonium_energy_1S = {MESON_1S_ENERGY}")
N = 3

line_styles = ['dotted', 'dashdot', 'dashed']

print("Solving")
wfns = []
for n in [1, 2, 3]:
    for l in range(0, n):
        E, sol = numericalSolvers.solve_for_energy(
            U0, r, corenell_wave_function, n,
            potential_arguments=(l, calibrated_variable, REDUCED_MESON_MASS),
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
        
        plt.plot(r, pdf, linestyle = line_styles[l%len(line_styles)], label = f"{n}{l}")
        print(f"E_{n}{l} = {E}")
        # print(f"M_{n}{l} = {E+2*charm_quark_mass}")
        last_energy_value = E

# for i in range(len(wfns)-1):
#     print(np.array_equal(wfns[i], wfns[i+1]))

plt.legend()
plt.show()


