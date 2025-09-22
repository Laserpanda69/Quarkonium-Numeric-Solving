import numpy as np  
import matplotlib.pyplot as plt

from Particles.Fermions.Quarks import *
from Particles.Hadrons import Mesons 

import numericalSolvers

import wavefuncitons as Wfns
import potentialModels as Vmods
from potentialModels import r_0_calc, r_1_calc, r_2_calc

from linestyles import LineStyle, line_styles_dict, line_styles_list

from massSolver import calculate_meson_masses

# https://pdg.lbl.gov/

GROUND_STATE = (1,0)
REFERENCE = 'reference'
STAIRCASE = 'staircase'
U0 = [0,1]


r_space = np.linspace(0.0000001, 15, 1000)

# Fix this so 1S state can be entered
charmonium_1S = Mesons.Charmonium(GROUND_STATE)
initial_calibration_var_charmonium_cornell = 0.195
initial_calibration_var_charmonium_bh = 0.2
initial_calibration_var_charmonium_rf = 0.3


bottomonium_1S = Mesons.Bottomonium(GROUND_STATE)
initial_calibration_var_bottomonium_cornell = 0.006
# bottomonium = Mesons.Toponium(GROUND_STATE)
# initial_calibration_var_toponium_cornell = 0.1

# User set variables
state_count = 3
F = 30
REDNER = False
meson = charmonium_1S
wavefunction = Wfns.bhanot_rudaz_wave_function
initial_calibration_variable = initial_calibration_var_charmonium_bh
# /User set variables

fig, axs = plt.subplots(ncols=2, nrows=1)

# Grey line at 0
plt.plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey") 

###########################################
##### POTENTIAL PARAMETER CALIBRATION #####
###########################################

print("Calibrating")
cornel_beta, sol, points_of_interest, error_on_cornell_beta = numericalSolvers.calibrate(
        U0, r_space, wavefunction, 
        potential_arguments= (meson.binding_energy, meson.reduced_mass),
        initial_calibration_variable = initial_calibration_variable, 
        flight = F
    )


print(f"calibration got {cornel_beta}")
pdf, u, v = sol
axs[0].plot(r_space, pdf, color = 'magenta', linestyle = line_styles_dict[LineStyle.LOOSELY_DASHDOTTED], linewidth = 4, label = "calibration")

binding_energies, masses_errors = calculate_meson_masses(meson, r_space, wavefunction, state_count, cornel_beta, ax = axs[0])
for n in range(state_count+1):
    for l in range(n):
        print(f"M_{n}{l} = {masses_errors[n][l][0]} +/- {masses_errors[n][l][1]}")
        
##################################
####### Cornel Calibrating #######
##################################

print("Calibrating Bhnot Rudaz")
cornell_beta, sol, points_of_interest, error_on_cornell_beta = numericalSolvers.calibrate(
        U0, r_space, Wfns.corenell_wave_function, 
        potential_arguments= (meson.binding_energy, meson.reduced_mass),
        initial_calibration_variable = initial_calibration_variable, 
        flight = F
    )

print(f"Cornell: {cornel_beta}")
        
##################################
######### BH Calibrating #########
##################################

print("Calibrating Bhnot Rudaz")
bh_beta, sol, points_of_interest, error_on_bh_beta = numericalSolvers.calibrate(
        U0, r_space, Wfns.bhanot_rudaz_wave_function, 
        potential_arguments= (meson.binding_energy, meson.reduced_mass),
        initial_calibration_variable = initial_calibration_variable, 
        flight = F
    )

print(f"Bhnot Rudaz: {bh_beta}")


##################################
######### RF Calibrating #########
##################################

print("Calibrating Richardson Fulcher")
rf_beta, sol, points_of_interest, error_on_rf_beta = numericalSolvers.calibrate(
        U0, r_space, Wfns.richerdson_fulcher_wave_function, 
        potential_arguments= (meson.binding_energy, meson.reduced_mass),
        initial_calibration_variable = initial_calibration_variable, 
        flight = F
    )

print(f"Richardson Fulcher: {rf_beta}")


##################################
######## Read Calibrating ########
##################################

print("Calibrating Read")
read_beta, sol, points_of_interest, error_on_read_beta = numericalSolvers.calibrate(
        U0, r_space, Wfns.read_wave_function, 
        potential_arguments= (meson.binding_energy, meson.reduced_mass),
        initial_calibration_variable = initial_calibration_variable, 
        flight = F
    )

print(f"Read: {read_beta}")

##################################
##### POTENTIAL PDF PLOTTING #####
##################################
color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# Plot y = 0
potential_cutoff = 10
axs[1].plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey")

# Plot cornell potential
potential_values = Vmods.cornell_potential(r_space, cornel_beta)
# cornell_roof = [val+error_on_cornell_beta for val in potential_values]
# cornell_floor = [val-error_on_cornell_beta for val in potential_values]
axs[1].plot(r_space[potential_cutoff:], potential_values[potential_cutoff:], label = "Cornell")
# axs[1].plot(r_space[potential_cutoff:], cornell_roof[potential_cutoff:], color = color_cycle[0], alpha = 0.3)
# axs[1].plot(r_space[potential_cutoff:], cornell_floor[potential_cutoff:], color = color_cycle[0], alpha = 0.3)
# axs[1].fill_between(r_space[potential_cutoff:], cornell_roof[potential_cutoff:], cornell_floor[potential_cutoff:],
#     color = color_cycle[0], alpha = 0.1)



# Plot BH potential
potential_values = [Vmods.bhanot_rudaz_potential(r, bh_beta) for r in r_space]
axs[1].plot(r_space[potential_cutoff:], potential_values[potential_cutoff:], label = "Bhanot Rudaz", linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED])

v_min = min(potential_values[potential_cutoff:])
v_max = max(potential_values[potential_cutoff:])

axs[1].vlines(r_0_calc(bh_beta), ymin = v_min, ymax = v_max, color = "gainsboro", linestyle = line_styles_dict[LineStyle.LONG_DASH_WITH_OFFSET])
axs[1].vlines(r_1_calc(bh_beta), ymin = v_min, ymax = v_max, color = "gainsboro", linestyle = line_styles_dict[LineStyle.LONG_DASH_WITH_OFFSET])
axs[1].vlines(r_2_calc(bh_beta), ymin = v_min, ymax = v_max, color = "gainsboro", linestyle = line_styles_dict[LineStyle.LONG_DASH_WITH_OFFSET])

# Plot RF potential
potential_values = Vmods.richerdson_fulcher_potential(r_space, rf_beta)
axs[1].plot(r_space[potential_cutoff+2:], potential_values[potential_cutoff+2:], label = "Richardson Fulcher", linestyle = line_styles_dict[LineStyle.DASHDOTTED])

# Plot Read potential
potential_values = Vmods.read_potential(r_space, 0.2)
axs[1].plot(r_space[potential_cutoff+2:], potential_values[potential_cutoff+2:], label = "Read", linestyle = line_styles_dict[LineStyle.DASHDOTTED])


##############################
##### MESON PDF PLOTTING #####
##############################

# Numerical solving of exciterd states


plt.legend()
plt.show()






