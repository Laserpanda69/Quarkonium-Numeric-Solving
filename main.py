import numpy as np  
import matplotlib.pyplot as plt
import scipy.integrate 

import wavefuncitons as wfns

from enum import Enum
from data import ParticleName, particle_masses, ColorCharge

import numericalSolvers as Solvers

from Particles.Fermions.Quarks import *
from Particles.Hadrons.Hadron import Hadron
from Particles.Hadrons import Mesons 

import numericalSolvers

from wavefuncitons import corenell_wave_function, bhanot_rudaz_wave_function
from potentialModels import cornell_potential, bhanot_rudaz_potential

from linestyles import LineStyle, line_styles_dict, line_styles_list

from massSolver import calculate_meson_masses

# https://pdg.lbl.gov/

GROUND_STATE = '1S'
REFERENCE = 'reference'
STAIRCASE = 'staircase'
U0 = [0,1]


r_space = np.linspace(0.0000001, 15, 1000)

# Fix this so 1S state can be entered
charmonium_1S = Mesons.Charmonium(GROUND_STATE)
initial_calibration_var_charmonium_cornell = 0.195

bottomonium_1S = Mesons.Bottomonium(GROUND_STATE)
initial_calibration_var_bottomonium_cornell = 0.006
# bottomonium = Mesons.Toponium(GROUND_STATE)
# initial_calibration_var_toponium_cornell = 0.1

# User set variables
N = 3
F = 30
REDNER = False
initial_calibration_variable = initial_calibration_var_charmonium_cornell
meson = charmonium_1S
wavefunction = bhanot_rudaz_wave_function
potential_model = bhanot_rudaz_potential
# /User set variables

# Grey line at 0

if REDNER:
    plt.plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey") 

###########################################
##### POTENTIAL PARAMETER CALIBRATION #####
###########################################

print("Calibrating")
calibrated_variable, sol, points_of_interest = numericalSolvers.calibrate(
        U0, r_space, wavefunction, 
        potential_arguments= (meson.binding_energy, meson.reduced_mass),
        initial_calibration_variable = initial_calibration_variable, 
        flight = F
    )

print(f"calibration got {calibrated_variable}")
pdf, u, v = sol
plt.plot(r_space, pdf, color = 'magenta', linestyle = line_styles_dict[LineStyle.LOOSELY_DASHDOTTED], linewidth = 4, label = "calibration")

binding_energies, masses = calculate_meson_masses(meson, r_space, wavefunction, N, calibrated_variable, render=REDNER)

for n in range(N+1):
    for l in range(n):
        print(f"M_{n}{l} = {masses[n][l]}")

##################################
##### POTENTIAL PDF PLOTTING #####
##################################

# plt.plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey")

# potential_values = [potential_model(r, calibrated_variable) for r in r_space]
# plt.plot(r_space[3:], potential_values[3:])

##############################
##### MESON PDF PLOTTING #####
##############################

# Numerical solving of exciterd states

if REDNER:
    plt.legend()
    plt.show()






