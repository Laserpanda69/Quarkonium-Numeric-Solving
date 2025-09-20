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

from linestyles import LineStyle, line_styles_dict, line_styles_list

# https://pdg.lbl.gov/

GROUND_STATE = '1S'
REFERENCE = 'reference'
STAIRCASE = 'staircase'
U0 = [0,1]

N = 3
F = 30
initial_calibration_variable = 2
r_space = np.linspace(0.0000001, 15, 1000)

# Fix this so 1S state can be entered
charmonium = Quarkonia("1S", CharmQuark(1/2, ColorCharge.RED), AntiCharmQuark(1/2, ColorCharge.RED))
charmonium.set_mass(particle_masses[ParticleName.CHARMONIUM][REFERENCE][GROUND_STATE])
initial_calibration_var_charmonium_cornell = 0.195


bottomonium = Quarkonia("10", BottomQuark(1/2, ColorCharge.RED), AntiBottomQuark(1/2, ColorCharge.RED))
bottomonium.set_mass(particle_masses[ParticleName.BOTTOMONIUM][REFERENCE][GROUND_STATE])
initial_calibration_var_bottomonium_cornell = 1.5

initial_calibration_variable = initial_calibration_var_charmonium_cornell

MESON_1S_MASS = charmonium.mass
recpricol_reduced_mass = sum(1/quark.mass for quark in charmonium.quarks)
REDUCED_MESON_MASS = 1/recpricol_reduced_mass
MESON_1S_ENERGY = MESON_1S_MASS - sum(quark.mass for quark in charmonium.quarks)

plt.plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey")


print("Calibrating")
calibrated_variable, sol = numericalSolvers.calibration_staircase(
        U0, r_space, corenell_wave_function, 
        potential_arguments= (MESON_1S_ENERGY, REDUCED_MESON_MASS),
        b_lower = initial_calibration_variable, 
        flight = F
    )
print(f"calibration got {calibrated_variable}")
u, v= sol[:,0], sol[:,1]
pdf = wfns.square_wavefunction(u)
pdf, u, v = wfns.normalise_wavefunction(r_space, pdf, u, v)
plt.plot(r_space, pdf, color = 'magenta', linestyle = line_styles_dict[LineStyle.LOOSELY_DASHDOTTED], linewidth = 4, label = "calibration")

last_energy_value = MESON_1S_ENERGY - 0.1
offset = 0.01
print(f"charmonium_energy_1S = {MESON_1S_ENERGY}")

print("Solving")
color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
for n in range(1, N+1):
    for l in range(0, n):
        E, sol, points_of_interest = numericalSolvers.solve_for_energy(
            U0, r_space, corenell_wave_function, n,
            potential_arguments=(l, calibrated_variable, REDUCED_MESON_MASS),
            epsilon_lower = last_energy_value + offset, 
            flight = F
        )
        pdf, u, v = sol
        nodes, turning_points = points_of_interest

        color = color_cycle[n-1]
        linestyle = line_styles_list[l]
        plt.plot(r_space, pdf, color = color, linestyle = linestyle, label = f"{n}{l}")
        
        pdf_maxima = 0
        # pdf_maximak_line = []

        if l == 0:
            pdf_turning_point_peaks = wfns.find_pdf_peaks(r_space, pdf, turning_points['positions'])
            
            plt.scatter(turning_points['positions'], pdf_turning_point_peaks, color = color, linewidths= .5)

            pdf_maxima = max(pdf_turning_point_peaks)
            pdf_maxima_line = [pdf_maxima]*len(r_space)
            plt.plot(r_space, pdf_maxima_line, 
                linestyle = line_styles_dict[LineStyle.LOOSELY_DOTTED], color = color, alpha = 0.4)
                
        elif l == n-1:
            pdf_turning_point_peaks = wfns.find_pdf_peaks(r_space, pdf, turning_points['positions'])

            tollerance = 0.01
            for i, amp in enumerate(pdf_turning_point_peaks):
                if amp < tollerance:
                    pdf_turning_point_peaks.pop(i)
                    turning_points['positions'].pop(i)

            plt.scatter(turning_points['positions'], pdf_turning_point_peaks, color = color, linewidths= .5)
            
            min_tp_peak = min(pdf_turning_point_peaks)
            min_tp_peak_line = [min_tp_peak]*len(r_space)
            plt.plot(r_space, min_tp_peak_line, 
                linestyle = line_styles_dict[LineStyle.LOOSELY_DOTTED], color = color, alpha = 0.4)

            plt.fill_between(r_space, min_tp_peak_line, pdf_maxima_line, where=(min_tp_peak < pdf_maxima_line), color=color, alpha=0.1)
            


            
        print(f"E_{n}{l} = {E}")
        # print(f"M_{n}{l} = {E+2*charm_quark_mass}")
        last_energy_value = E

# for i in range(len(wfns)-1):
#     print(np.array_equal(wfns[i], wfns[i+1]))

plt.legend()
plt.show()






