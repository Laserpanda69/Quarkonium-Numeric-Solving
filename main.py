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
from potentialModels import cornell_potential, bhanot_rudaz_potential, r_0_calc, r_1_calc, r_2_calc

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
# /User set variables

fig, axs = plt.subplots(ncols=2, nrows=1)

# Grey line at 0
plt.plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey") 

###########################################
##### POTENTIAL PARAMETER CALIBRATION #####
###########################################

print("Calibrating")
cornel_beta, sol, points_of_interest = numericalSolvers.calibrate(
        U0, r_space, corenell_wave_function, 
        potential_arguments= (meson.binding_energy, meson.reduced_mass),
        initial_calibration_variable = initial_calibration_variable, 
        flight = F
    )


print(f"calibration got {cornel_beta}")
pdf, u, v = sol
axs[0].plot(r_space, pdf, color = 'magenta', linestyle = line_styles_dict[LineStyle.LOOSELY_DASHDOTTED], linewidth = 4, label = "calibration")



binding_energies, masses = calculate_meson_masses(meson, r_space, corenell_wave_function, N, cornel_beta, ax = axs[0])
for n in range(N+1):
    for l in range(n):
        print(f"M_{n}{l} = {masses[n][l]}")
        
##################################
######### BH Calibrating #########
##################################

print("Calibrating")
bh_beta, sol, points_of_interest = numericalSolvers.calibrate(
        U0, r_space, bhanot_rudaz_wave_function, 
        potential_arguments= (meson.binding_energy, meson.reduced_mass),
        initial_calibration_variable = initial_calibration_variable, 
        flight = F
    )

##################################
##### POTENTIAL PDF PLOTTING #####
##################################

potential_cutoff = 3
axs[1].plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey")

potential_values = cornell_potential(r_space, cornel_beta)
axs[1].plot(r_space[potential_cutoff:], potential_values[potential_cutoff:], label = "Cornell")


potential_values = [bhanot_rudaz_potential(r, bh_beta) for r in r_space]
axs[1].plot(r_space[potential_cutoff:], potential_values[potential_cutoff:], label = "Bhanot Rudaz", linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED])

v_min = min(potential_values[potential_cutoff:])
v_max = max(potential_values[potential_cutoff:])

axs[1].vlines(r_0_calc(bh_beta), ymin = v_min, ymax = v_max, color = "gainsboro", linestyle = line_styles_dict[LineStyle.LONG_DASH_WITH_OFFSET])
axs[1].vlines(r_1_calc(bh_beta), ymin = v_min, ymax = v_max, color = "gainsboro", linestyle = line_styles_dict[LineStyle.LONG_DASH_WITH_OFFSET])
axs[1].vlines(r_2_calc(bh_beta), ymin = v_min, ymax = v_max, color = "gainsboro", linestyle = line_styles_dict[LineStyle.LONG_DASH_WITH_OFFSET])

# axs[1].vlines(5, ymin = -10, ymax = 10, color = "grey", linestyle = line_styles_dict[LineStyle.LONG_DASH_WITH_OFFSET])

##############################
##### MESON PDF PLOTTING #####
##############################

# Numerical solving of exciterd states


plt.legend()
plt.show()






