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
initial_calibration_variable = initial_calibration_var_charmonium_cornell
meson = charmonium_1S
wavefunction = bhanot_rudaz_wave_function
potential_model = bhanot_rudaz_potential
# /User set variables

# Grey line at 0

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

last_energy_value = meson.binding_energy - 0.1
offset = 0.01

print("Solving")
color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
for n in range(1, N+1):
    pdf_maxima = 0
    min_tp_peak = 100
    for l in range(0, n):
        E, sol, points_of_interest = numericalSolvers.solve_for_energy(
            U0, r_space, wavefunction, n,
            potential_arguments=(l, calibrated_variable, meson.reduced_mass),
            epsilon_lower = last_energy_value + offset, 
            flight = F
        )
        pdf, u, v = sol
        nodes, turning_points = points_of_interest

        color = color_cycle[n-1]
        linestyle = line_styles_list[l]
        plt.plot(r_space, pdf, color = color, linestyle = linestyle, label = f"{n}{l}")

        # pdf_maximak_line = []
        
        if n == 1:
            print(f"numerically solved meson ground state energy = {meson.binding_energy}")
            print(f"reference meson energy = {meson.binding_energy}")
            print(f"Delta = {meson.binding_energy - E}")
            print("")
            
        pdf_turning_point_peaks = wfns.find_pdf_peaks(r_space, pdf, turning_points['positions'])


        local_maxima = max(pdf_turning_point_peaks)
        pdf_maxima =  local_maxima if local_maxima > pdf_maxima else pdf_maxima
        pdf_maxima_line = [pdf_maxima]*len(r_space)
        
        plt.plot(r_space, pdf_maxima_line, 
            linestyle = line_styles_dict[LineStyle.LOOSELY_DOTTED], color = color, alpha = 0.4)



        tollerance = 0.01
        for i, amp in enumerate(pdf_turning_point_peaks):
            if amp < tollerance:
                pdf_turning_point_peaks.pop(i)
                turning_points['positions'].pop(i)

        plt.scatter(turning_points['positions'], pdf_turning_point_peaks, color = color, linewidths= .5)
        
        local_lowest_peak = min(pdf_turning_point_peaks)
        min_tp_peak = local_lowest_peak if local_lowest_peak < min_tp_peak else min_tp_peak
        min_tp_peak_line = [min_tp_peak]*len(r_space)
        plt.plot(r_space, min_tp_peak_line, 
            linestyle = line_styles_dict[LineStyle.LOOSELY_DOTTED], color = color, alpha = 0.4)

            


            
        print(f"E_{n}{l} = {E}")
        # print(f"M_{n}{l} = {E+2*charm_quark_mass}")
        last_energy_value = E
    plt.fill_between(r_space, min_tp_peak_line, pdf_maxima_line, where=(min_tp_peak < pdf_maxima_line), color=color, alpha=0.1)



plt.legend()
plt.show()






