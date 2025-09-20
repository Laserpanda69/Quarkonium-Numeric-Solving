import scipy.integrate 
import wavefuncitons as wfns
import numpy as np


# def while_staircase_solver(u0, radii, wave_function, alpha, fixed_value, reduced_mass, epsilon, step_size = 0.015, flight = 5, calibration_mode = False):
#     # epsilon is beta in calibration mode and energy if not
#     # fixed value is the inverse
#     divergence_has_flipped = False
#     steps_taken = 0
#     while not divergence_has_flipped:
        
#         epsilon_lower = epsilon + (step_size * steps_taken)

#         args= (1,0,alpha,epsilon_lower, reduced_mass, fixed_value) if calibration_mode \
#             else (1,0,alpha, fixed_value, reduced_mass, epsilon_lower)
        
#         sol = scipy.integrate.odeint(wave_function, u0, radii, args = args)
#         v1 = sol[:,1]
        
#         # Takes step
#         steps_taken += 1
        
#         epsilon_upper = epsilon + (step_size * steps_taken)
#         args= (1,0,alpha,epsilon_upper, reduced_mass, fixed_value) if calibration_mode \
#             else (1,0,alpha, fixed_value, reduced_mass, epsilon_upper)
#         sol = scipy.integrate.odeint(wave_function, u0, radii, args=args)
#         v2 = sol[:,1]
        
#         divergence_has_flipped = (v1[-1] < 0) != (v2[-1] < 0)
        
#     gamma = (epsilon_lower+epsilon_upper)/2

#     if flight > 0:
#         return while_staircase_solver(u0, radii, wave_function, alpha, fixed_value, reduced_mass, epsilon = epsilon_lower, step_size=step_size/2, flight= flight -1, calibration_mode=calibration_mode)
    
#     args= (1,0,alpha,gamma, reduced_mass, fixed_value) if calibration_mode \
#         else (1,0,alpha, fixed_value, reduced_mass, gamma)
#     return gamma, scipy.integrate.odeint(wave_function, u0, radii, args= args)

    
def nodes_turning_points(u, v, r):

    def zero_crossings(f, x) -> dict:
        positions = []
        for i in range(1, len(f)):
            if (f[i-1] < 0 and f[i] > 0) or (f[i-1] > 0 and f[i] < 0):
                xi = x[i-1] - f[i-1] * (x[i] - x[i-1]) / (f[i] - f[i-1])
                positions.append(xi)
        return positions
    
    # Nodes and turning points may get false positives due to values near 0 at start of wavefunction
    offset = 0
    node_positions = zero_crossings(u[offset:], r[offset:])
    turning_positions = zero_crossings(v[offset:], r[offset:])
    
    # Positions are positions on the r axis
    return {
        "nodes": {
            'count': len(node_positions),
            'positions': node_positions
            },
        "turning_points": {
            'count': len(turning_positions),
            'positions': turning_positions
        }
    }


def calibration_staircase(u0, r_space, wave_function, potential_arguments: tuple, b_lower, step_size = 0.015, steps_taken = 0, flight = 5):
    base_energy, reduced_mass = potential_arguments
    # Move epsilon, reduced mass, and fixed value into a tuple 
    # so other potentialls with differnt arguments can be used
    
    # This method not yet using calibration mode
    
    b_upper = b_lower + step_size * (steps_taken+1)
    v_lower = scipy.integrate.odeint(wave_function, u0, r_space, args=(0, b_lower, reduced_mass, base_energy))[:,1]
    v_upper = scipy.integrate.odeint(wave_function, u0, r_space, args=(0, b_upper, reduced_mass, base_energy))[:,1]
    
    divergence_has_flipped = (v_lower[-1] < 0) != (v_upper[-1] < 0)
    if not divergence_has_flipped:
        return calibration_staircase(u0, r_space, wave_function, potential_arguments, b_lower =b_upper,
            step_size= step_size, steps_taken= steps_taken+1, flight=flight)
    
    # print(layer)
    # Divergence has flipped
    if flight > 0:
        return calibration_staircase(u0, r_space, wave_function, potential_arguments, b_lower=b_lower,
            step_size = step_size/2, steps_taken = 0, flight = flight - 1)
    
    # Divergence has flipped and all layers have been run
    gamma = (b_lower+b_upper)/2
    return gamma, scipy.integrate.odeint(wave_function, u0, r_space, args=(0,gamma, reduced_mass, base_energy))

def energy_staircase(u0, r_space, wave_function, potential_arguments: tuple, epsilon_lower, step_size = 0.015, steps_taken = 0, flight = 5):
    l, beta, reduced_mass = potential_arguments
    # Move epsilon, reduced mass, and fixed value into a tuple 
    # so other potentialls with differnt arguments can be used
    
    # This method not yet using calibration mode
    
    epsilon_upper = epsilon_lower + step_size * (steps_taken+1)
    v_lower = scipy.integrate.odeint(wave_function, u0, r_space, args=(l, beta, reduced_mass, epsilon_lower))[:,1]
    v_upper = scipy.integrate.odeint(wave_function, u0, r_space, args=(l, beta, reduced_mass, epsilon_upper))[:,1]
    
    divergence_has_flipped = (v_lower[-1] < 0) != (v_upper[-1] < 0)
    
    if not divergence_has_flipped:
        return energy_staircase(u0, r_space, wave_function, potential_arguments, epsilon_lower =epsilon_upper,
            step_size= step_size, steps_taken= steps_taken+1, flight=flight)
    
    gamma = (epsilon_lower+epsilon_upper)/2
    # print(gamma)
    # print(layer)
    # Divergence has flipped
    if flight > 0:
        # print("going to flight",flight )
        return energy_staircase(u0, r_space, wave_function, potential_arguments, epsilon_lower=epsilon_lower,
            step_size = step_size/2, steps_taken = 0, flight = flight - 1)
    
    # Divergence has flipped and all layers have been run
        
    return gamma, scipy.integrate.odeint(wave_function, u0, r_space, args=(l,beta, reduced_mass, gamma))


def calibrate(u0, r_space, wave_function, potential_arguments: tuple, initial_calibration_variable, step_size = 0.015, steps_taken = 0, flight = 5, energy_offset = 0.01):
    
    calibrated_variable, numeric_solution = calibration_staircase(u0, r_space, wave_function, potential_arguments, initial_calibration_variable, step_size, steps_taken, flight)
    u = numeric_solution[:,0]
    v = numeric_solution[:,1]

    
    nodes_tps  = nodes_turning_points(u, v, r_space)
    nodes = nodes_tps.pop('nodes')
    turning_points = nodes_tps.pop('turning_points')

    pdf = wfns.square_wavefunction(u)
    pdf, u, v = wfns.normalise_wavefunction(r_space, pdf, u, v)
    
    return calibrated_variable, (pdf, u ,v), (nodes, turning_points)

def solve_for_energy(u0, r_space, wave_function, n, potential_arguments: tuple, epsilon_lower, step_size = 0.015, steps_taken = 0, flight = 5, energy_offset = 0.01):
    
    energy, numeric_solution = energy_staircase(u0, r_space, wave_function, potential_arguments, epsilon_lower, step_size, steps_taken, flight)
    u = numeric_solution[:,0]
    v = numeric_solution[:,1]

    
    nodes_tps  = nodes_turning_points(u, v, r_space)
    nodes = nodes_tps.pop('nodes')
    turning_points = nodes_tps.pop('turning_points')

    pdf = wfns.square_wavefunction(u)
    pdf, u, v = wfns.normalise_wavefunction(r_space, pdf, u, v)
    
    return energy, (pdf, u ,v), (nodes, turning_points)