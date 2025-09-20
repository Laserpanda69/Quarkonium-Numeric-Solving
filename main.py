import numpy as np  
import matplotlib.pyplot as plt
import scipy.integrate 

import wavefuncitons as wfns

from enum import Enum
from data import ParticleName, particle_masses, ColorCharge

import numericalSolvers as Solvers

from Particles.Fermions.Quarks import *
from Particles.Hadrons.Hadron import Hadron
from Particles.Hadrons.Mesons import Meson, Quarkonia

import numericalSolvers

from wavefuncitons import corenell_wave_function, bhanot_rudaz_wave_function

# https://pdg.lbl.gov/

U0 = [0,1]
initial_calibration_variable = 2
r = np.linspace(0.0000001, 15, 1000)

# Fix this so 1S state can be entered
charmonium = Quarkonia("1S", CharmQuark(1/2, ColorCharge.RED), AntiCharmQuark(1/2, ColorCharge.RED))
charmonium.set_mass(particle_masses[ParticleName.CHARMONIUM]['reference']['1S'])
initial_calibration_var_charmonium_cornell = 0.195


bottomonium = Quarkonia("10", BottomQuark(1/2, ColorCharge.RED), AntiBottomQuark(1/2, ColorCharge.RED))
bottomonium.set_mass(particle_masses[ParticleName.BOTTOMONIUM]['reference']['1S'])
initial_calibration_var_bottomonium_cornell = 1.5

initial_calibration_variable = initial_calibration_var_charmonium_cornell

MESON_1S_MASS = charmonium.mass
recpricol_reduced_mass = sum(1/quark.mass for quark in charmonium.quarks)
REDUCED_MESON_MASS = 1/recpricol_reduced_mass
MESON_1S_ENERGY = MESON_1S_MASS - sum(quark.mass for quark in charmonium.quarks)



print("Calibrating")
calibrated_variable, sol = numericalSolvers.calibration_staircase(
        U0, r, corenell_wave_function, 
        potential_arguments= (MESON_1S_ENERGY, REDUCED_MESON_MASS),
        b_lower = initial_calibration_variable, 
        flight = 50
    )
print(f"calibration got {calibrated_variable}")
u, v= sol[:,0], sol[:,1]
pdf = wfns.square_wavefunction(u)
pdf, u, v = wfns.normalise_wavefunction(r, pdf, u, v)
plt.plot(r, pdf, label = "calibration")

last_energy_value = MESON_1S_ENERGY - 0.1
offset = 0.01
print(f"charmonium_energy_1S = {MESON_1S_ENERGY}")
N = 3

line_styles = ['dotted', 'dashdot', 'dashed']

print("Solving")
for n in [1, 2, 3]:
    for l in range(0, n):
        E, sol = numericalSolvers.solve_for_energy(
            U0, r, corenell_wave_function, n,
            potential_arguments=(l, calibrated_variable, REDUCED_MESON_MASS),
            epsilon_lower = last_energy_value + offset, 
            flight = 50
        )
        u = sol[:,0]
        v= sol[:,1]
                
        pdf = wfns.square_wavefunction(u)
        pdf, u, v = wfns.normalise_wavefunction(r, pdf, u, v)
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




