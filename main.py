import numpy as np  
import matplotlib.pyplot as plt
import scipy.integrate 

from wavefuncitons import corenell_wave_function

from enum import Enum
from quarkData import ParticleNames, quark_masses, quarkonium_masses




def count_nodes_and_turns(u,v,r):
    node_count = 0
    turn_count = 0
    for i in range(len(r) -1):
        cross_up = u[i] <= 0 and u[i+1] >= 0
        cross_down = u[i] >= 0 and u[i+1] <= 0
        
        turn_up = v[i] >= 0 and v[i+1] <= 0
        turn_down = v[i] <= 0 and v[i+1] >= 0
        
        if cross_up or cross_down:
            node_count += 1
        if turn_up or turn_down:
            turn_count +=1
            
    return node_count, turn_count

U0 = [0,1]
alpha = 0.4
init_beta = 0.195

charm_quark_mass = 1.27
charmonium_mass_1S = 2.9839

charmonium_energy_1S = charmonium_mass_1S - 2*charm_quark_mass
#mu = mc/2

recpricol_reduced_mass = 1/charm_quark_mass + 1/charm_quark_mass
reduced_mass = 1/recpricol_reduced_mass
r = np.linspace(0.0000001, 15, 10000)

    # unexcited_state_energy = quarkonium_masses[particle_name]['1S'] - 2*quark_masses[particle_name]


def while_staircase_solver(u0, radii, wave_function, alpha, fixed_value, epsilon, step_size = 0.015, flight = 5, calibration_mode = False):
    # epsilon is beta in calibration mode and energy if not
    # fixed value is the inverse
    divergence_has_flipped = False
    steps_taken = 0
    while not divergence_has_flipped:
        
        epsilon_lower = epsilon + (step_size * steps_taken)

        args= (1,0,alpha,epsilon_lower, reduced_mass, fixed_value) if calibration_mode \
            else (1,0,alpha, fixed_value, reduced_mass, epsilon_lower)
        
        sol = scipy.integrate.odeint(wave_function, u0, radii, args = args)
        v1 = sol[:,1]
        
        # Takes step
        steps_taken += 1
        
        epsilon_upper = epsilon + (step_size * steps_taken)
        args= (1,0,alpha,epsilon_upper, reduced_mass, fixed_value) if calibration_mode \
            else (1,0,alpha, fixed_value, reduced_mass, epsilon_upper)
        sol = scipy.integrate.odeint(wave_function, u0, radii, args=args)
        v2 = sol[:,1]
        
        divergence_has_flipped = (v1[-1] < 0) != (v2[-1] < 0)
        
    gamma = (epsilon_lower+epsilon_upper)/2

    if flight > 0:
        return while_staircase_solver(u0, radii, wave_function, alpha, fixed_value, epsilon = epsilon_lower, step_size=step_size/2, flight= flight -1, calibration_mode=calibration_mode)
    
    args= (1,0,alpha,gamma, reduced_mass, fixed_value) if calibration_mode \
        else (1,0,alpha, fixed_value, reduced_mass, gamma)
    return gamma, scipy.integrate.odeint(wave_function, u0, radii, args= args)

# epsilon lower is given aqnd not calculated as it avoids calculating all values twice
def recursive_staircase_solver(u0, alpha, epsilon_lower, fixed_value, wave_function, calibration_mode = False, step_size = 0.015, steps_taken = 0, flight = 5):
    epsilon_upper = epsilon_lower + step_size * (steps_taken+1)
    v_lower = scipy.integrate.odeint(wave_function, u0, r, args=(1,0,alpha,epsilon_lower, reduced_mass, fixed_value))[:,0]
    v_upper = scipy.integrate.odeint(wave_function, u0, r, args=(1,0,alpha,epsilon_upper, reduced_mass, fixed_value))[:,0]
    
    divergence_has_flipped = (v_lower[-1] < 0) != (v_upper[-1] < 0)
    if not divergence_has_flipped:
        return recursive_staircase_solver(u0, epsilon_upper, fixed_value, step_size= step_size, steps_taken= steps_taken+1, flight=flight)
    
    # print(layer)
    # Divergence has flipped
    if flight > 0:
        return recursive_staircase_solver(u0, epsilon_lower, fixed_value, step_size = step_size/2, steps_taken = 0, flight = flight - 1)
    
    # Divergence has flipped and all layers have been run
    gamma = (epsilon_lower+epsilon_upper)/2
    return gamma, scipy.integrate.odeint(wave_function, u0, r, args=(1,0,alpha,gamma, reduced_mass, fixed_value))
    
# beta, sol = recursive_staircase_solver(U0, alpha, epsilon_lower=init_beta, fixed_value=charmonium_energy_1S, layer=30)
beta, sol = while_staircase_solver(U0, r, corenell_wave_function, alpha, charmonium_energy_1S, init_beta, flight = 30, calibration_mode=True)
u = sol[:,0]



print(beta)
plt.plot(r, u)
plt.show()


