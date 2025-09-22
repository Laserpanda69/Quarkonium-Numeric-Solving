import matplotlib.pyplot as plt

import wavefuncitons as wfns


from Particles.Fermions.Quarks import *
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

# Grey line at 0

def calculate_meson_masses(meson: Mesons.Meson,r_space,wavefunction,n_states_count,
    calibrated_variable,flights=30, ax = None
) -> tuple[dict]:

    if ax:
        ax.plot(r_space, [0]*len(r_space), linestyle = line_styles_dict[LineStyle.LOOSELY_DASHED], color = "grey")

    ##############################
    ##### MESON PDF PLOTTING #####
    ##############################

    # Numerical solving of exciterd states

    last_energy_value = meson.binding_energy - 0.1
    offset = 0.01

    print("Solving")
    color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    binding_energies = [[]]
    masses = [[]]

    for n in range(1, n_states_count+1):
        binding_energies.append([])
        masses.append([])
        
        pdf_maxima = 0
        min_tp_peak = 100
        
        for l in range(0, n):
            binding_energy, sol, points_of_interest, energy_error = numericalSolvers.solve_for_energy(
                U0, r_space, wavefunction, n,
                potential_arguments=(l, calibrated_variable, meson.reduced_mass),
                epsilon_lower = last_energy_value + offset, 
                flight = flights
            )
            pdf, u, v = sol

            # print(f"E_{n}{l} = {E}")
            # print(f"M_{n}{l} = {E+2*charm_quark_mass}")
            last_energy_value = binding_energy

            binding_energies[n].append((binding_energy, energy_error))
            quark_mass = sum(q.mass for q in meson.quarks)
            masses[n].append(binding_energy + quark_mass)

            if ax:
                nodes, turning_points = points_of_interest
                color = color_cycle[n-1]
                linestyle = line_styles_list[l]

                pdf_turning_point_peaks = wfns.find_pdf_peaks(r_space, pdf, turning_points['positions'])

                local_maxima = max(pdf_turning_point_peaks)
                pdf_maxima =  local_maxima if local_maxima > pdf_maxima else pdf_maxima
                pdf_maxima_line = [pdf_maxima]*len(r_space)

                tollerance = 0.01
                for i, amp in enumerate(pdf_turning_point_peaks):
                    if amp < tollerance:
                        pdf_turning_point_peaks.pop(i)
                        turning_points['positions'].pop(i)

                local_lowest_peak = min(pdf_turning_point_peaks)
                min_tp_peak = local_lowest_peak if local_lowest_peak < min_tp_peak else min_tp_peak
                min_tp_peak_line = [min_tp_peak]*len(r_space)

                ax.scatter(turning_points['positions'], pdf_turning_point_peaks, color = color, linewidths= .5)
                ax.plot(r_space, pdf, color=color, linestyle=linestyle, label=f"{n}{l}")
                ax.plot(r_space,pdf_maxima_line,linestyle=line_styles_dict[LineStyle.LOOSELY_DOTTED],color=color,alpha=0.4,)
                ax.plot(r_space, min_tp_peak_line, linestyle = line_styles_dict[LineStyle.LOOSELY_DOTTED], color = color, alpha = 0.4)

        if ax:
            ax.fill_between(r_space, min_tp_peak_line, pdf_maxima_line, where=(min_tp_peak < pdf_maxima_line), color=color, alpha=0.1)
            ax.legend()

    return binding_energies, masses
