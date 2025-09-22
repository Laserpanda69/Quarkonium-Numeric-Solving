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
charmonium_1S.set_mass(particle_masses[ParticleName.CHARMONIUM][REFERENCE][GROUND_STATE[0]][GROUND_STATE[1]]['value'])
initial_calibration_var_charmonium_cornell = 0.195
initial_calibration_var_charmonium_bh = 0.2
initial_calibration_var_charmonium_rf = 0.3


bottomonium_1S = Mesons.Bottomonium(GROUND_STATE)
initial_calibration_var_bottomonium_cornell = 0.006
# bottomonium = Mesons.Toponium(GROUND_STATE)
# initial_calibration_var_toponium_cornell = 0.1

# User set variables
state_count = 3
flights = 30
REDNER = False
ground_state_meson = charmonium_1S
wavefunction = Wfns.read_wave_function
initial_calibration_variable = 0.1
# /User set variables

fig, axs = plt.subplots(ncols=2, nrows=2)

# Grey line at 0
for ax in axs:
    for a in ax:
        a.plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey") 

##################################
####### Cornel Calibrating #######
##################################

print("Calibrating Cornell")
cornell_beta, sol, points_of_interest = numericalSolvers.calibrate(
        U0, r_space, Wfns.cornell_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )

print(f"Cornell: {cornell_beta}")
        
##################################
######### BH Calibrating #########
##################################

print("Calibrating Bhnot Rudaz")
bhanot_rudaz_beta, sol, points_of_interest = numericalSolvers.calibrate(
        U0, r_space, Wfns.bhanot_rudaz_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )

print(f"Bhnot Rudaz: {bhanot_rudaz_beta}")


##################################
######### RF Calibrating #########
##################################

print("Calibrating Richardson Fulcher")
richardson_fulcher_beta, sol, points_of_interest = numericalSolvers.calibrate(
        U0, r_space, Wfns.richardson_fulcher_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )

print(f"Richardson Fulcher: {richardson_fulcher_beta}")


##################################
######## Read Calibrating ########
##################################

print("Calibrating Read")
read_beta, sol, points_of_interest = numericalSolvers.calibrate(
        U0, r_space, Wfns.read_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )

print(f"Read: {read_beta}")

##################################
## Clcualte Masses and Plot PDF ##
##################################

axs[0,0].set_title("Cornell")
cornell_mesons = calculate_meson_masses(r_space, wavefunction=Wfns.calibrate_cornell_wave_function(cornell_beta[0]), 
    meson_type=Mesons.Charmonium, n_states_count=state_count, ax=axs[0,0])

axs[0,1].set_title("Bhanot Rudaz")
bhanot_rudaz_mesons = calculate_meson_masses(r_space, wavefunction=Wfns.calibrate_bhanot_rudaz_wave_function(bhanot_rudaz_beta[0]), 
    meson_type=Mesons.Charmonium, n_states_count=state_count, ax=axs[0,1])

axs[1,0].set_title("Richardson Fulcher")
richardson_fulcher_mesons = calculate_meson_masses(r_space, wavefunction=Wfns.calibrate_richardson_fulcher_wave_function(richardson_fulcher_beta[0]), 
    meson_type=Mesons.Charmonium, n_states_count=state_count, ax=axs[1,0])

axs[1,1].set_title("Read")
read_mesons = calculate_meson_masses(r_space, wavefunction=Wfns.calibrate_read_wave_function(read_beta[0]), 
    meson_type=Mesons.Charmonium, n_states_count=state_count, ax=axs[1,1])

plt.show()
import sys
sys.exit()
##################################
##### POTENTIAL PDF PLOTTING #####
##################################
color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# Plot y = 0
potential_cutoff = 10
axs[1].plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey")

# Plot cornell potential
potential_values = Vmods.cornell_potential(r_space, cornell_beta)
cornell_roof = [val+error_on_cornell_beta for val in potential_values]
cornell_floor = [val-error_on_cornell_beta for val in potential_values]
axs[1].plot(r_space[potential_cutoff:], potential_values[potential_cutoff:], label = "Cornell")
axs[1].plot(r_space[potential_cutoff:], cornell_roof[potential_cutoff:], color = color_cycle[0], alpha = 0.3)
axs[1].plot(r_space[potential_cutoff:], cornell_floor[potential_cutoff:], color = color_cycle[0], alpha = 0.3)
axs[1].fill_between(r_space[potential_cutoff:], cornell_roof[potential_cutoff:], cornell_floor[potential_cutoff:],
    color = color_cycle[0], alpha = 0.1)



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



plt.legend()
plt.show()






