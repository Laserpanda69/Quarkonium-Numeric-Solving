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
cornell_beta, sol, points_of_interest = numericalSolvers.calibrate_and_evaluate(
        U0, r_space, Wfns.cornell_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )
print(f"{cornell_beta= }")
calibrated_cornell_potential = Vmods.calibrate_potential_model(Vmods.cornell_potential, cornell_beta[0])
calibrated_cornell_wavefunction = Wfns.calibrate_wavefunction(calibrated_cornell_potential)

##################################
######### BH Calibrating #########
##################################

print("Calibrating Bhnot Rudaz")
bhanot_rudaz_beta, sol, points_of_interest = numericalSolvers.calibrate_and_evaluate(
        U0, r_space, Wfns.bhanot_rudaz_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )
print(f"{bhanot_rudaz_beta= }")
calibrated_bhanot_rudaz_potential = Vmods.calibrate_potential_model(Vmods.bhanot_rudaz_potential, bhanot_rudaz_beta[0])
calibrated_bhanot_rudaz_wavefunction = Wfns.calibrate_wavefunction(calibrated_bhanot_rudaz_potential)


##################################
######### RF Calibrating #########
##################################

print("Calibrating Richardson Fulcher")
richardson_fulcher_beta, sol, points_of_interest = numericalSolvers.calibrate_and_evaluate(
        U0, r_space, Wfns.richardson_fulcher_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )
print(f"{richardson_fulcher_beta= }")
calibrated_richardson_fulcher_potential = Vmods.calibrate_potential_model(Vmods.richardson_fulcher_potential, richardson_fulcher_beta[0])
calibrated_richardson_fulcher_wavefunction = Wfns.calibrate_wavefunction(calibrated_richardson_fulcher_potential)


##################################
######## Read Calibrating ########
##################################

print("Calibrating Read")
read_beta, sol, points_of_interest = numericalSolvers.polish_evaluation(
        U0, r_space, Wfns.read_wave_function, ground_state_meson,
        initial_beta_list = [0.1, 1], 
        flight = flights
    )
print(f"{read_beta= }")
calibrated_read_potential = Vmods.calibrate_potential_model(Vmods.read_potential, read_beta[0])
calibrated_read_wavefunction = Wfns.calibrate_wavefunction(calibrated_read_potential)


##################################
## Clcualte Masses and Plot PDF ##
##################################

axs[0,0].set_title("Cornell")
cornell_mesons = calculate_meson_masses(r_space, wavefunction=calibrated_cornell_wavefunction, 
    meson_type=Mesons.Charmonium, n_states_count=3, ax=axs[0,0])

axs[0,1].set_title("Bhanot Rudaz")
bhanot_rudaz_mesons = calculate_meson_masses(r_space, wavefunction=calibrated_bhanot_rudaz_wavefunction, 
    meson_type=Mesons.Charmonium, n_states_count=state_count, ax=axs[0,1])

axs[1,0].set_title("Richardson Fulcher")
richardson_fulcher_mesons = calculate_meson_masses(r_space, wavefunction=calibrated_richardson_fulcher_wavefunction, 
    meson_type=Mesons.Charmonium, n_states_count=state_count, ax=axs[1,0])

axs[1,1].set_title("Read")
read_mesons = calculate_meson_masses(r_space, wavefunction = calibrated_read_wavefunction, 
    meson_type=Mesons.Charmonium, n_states_count=state_count, ax=axs[1,1])

plt.show()

##################################
##### POTENTIAL PDF PLOTTING #####
##################################
color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# Plot y = 0
potential_cutoff = 10
plt.plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey")

# Plot cornell potential
potential_values = calibrated_cornell_potential(r_space)
# cornell_roof = [val+error_on_cornell_beta for val in potential_values]
# cornell_floor = [val-error_on_cornell_beta for val in potential_values]
plt.plot(r_space[potential_cutoff:], potential_values[potential_cutoff:], label = "Cornell")
# plt.plot(r_space[potential_cutoff:], cornell_roof[potential_cutoff:], color = color_cycle[0], alpha = 0.3)
# plt.plot(r_space[potential_cutoff:], cornell_floor[potential_cutoff:], color = color_cycle[0], alpha = 0.3)
# plt.fill_between(r_space[potential_cutoff:], cornell_roof[potential_cutoff:], cornell_floor[potential_cutoff:],
    # color = color_cycle[0], alpha = 0.1)



# Plot BH potential
potential_values = [calibrated_bhanot_rudaz_potential(r) for r in r_space]
plt.plot(r_space[potential_cutoff:], potential_values[potential_cutoff:], label = "Bhanot Rudaz", linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED])

v_min = min(potential_values[potential_cutoff:])
v_max = max(potential_values[potential_cutoff:])

plt.vlines(r_0_calc(bhanot_rudaz_beta[0]), ymin = v_min, ymax = v_max, color = "gainsboro", linestyle = line_styles_dict[LineStyle.LONG_DASH_WITH_OFFSET])
plt.vlines(r_1_calc(bhanot_rudaz_beta[0]), ymin = v_min, ymax = v_max, color = "gainsboro", linestyle = line_styles_dict[LineStyle.LONG_DASH_WITH_OFFSET])
plt.vlines(r_2_calc(bhanot_rudaz_beta[0]), ymin = v_min, ymax = v_max, color = "gainsboro", linestyle = line_styles_dict[LineStyle.LONG_DASH_WITH_OFFSET])

# Plot RF potential
potential_values = calibrated_richardson_fulcher_potential(r_space)
plt.plot(r_space[potential_cutoff+2:], potential_values[potential_cutoff+2:], label = "Richardson Fulcher", linestyle = line_styles_dict[LineStyle.DASHDOTTED])

# Plot Read potential
potential_values = calibrated_read_potential(r_space)
plt.plot(r_space[potential_cutoff+2:], potential_values[potential_cutoff+2:], label = "Read", linestyle = line_styles_dict[LineStyle.DASHDOTTED])



plt.legend()
plt.show()






