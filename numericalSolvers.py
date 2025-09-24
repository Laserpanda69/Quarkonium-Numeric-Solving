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


def calibration_staircase(u0, r_space, wave_function, meson_1S, b_lower, step_size = 0.015, steps_taken = 0, flight = 5):
    # Move epsilon, reduced mass, and fixed value into a tuple 
    # so other potentialls with differnt arguments can be used
    
    # This method not yet using calibration mode
    
    b_upper = b_lower + step_size * (steps_taken+1)
    v_lower = scipy.integrate.odeint(wave_function, u0, r_space, args=(meson_1S, b_lower))[:,1]
    v_upper = scipy.integrate.odeint(wave_function, u0, r_space, args=(meson_1S, b_upper))[:,1]
    
    divergence_has_flipped = (v_lower[-1] < 0) != (v_upper[-1] < 0)
    if not divergence_has_flipped:
        return calibration_staircase(u0, r_space, wave_function, meson_1S, b_lower =b_upper,
            step_size= step_size, steps_taken= steps_taken+1, flight=flight)
    
    # print(layer)
    # Divergence has flipped
    if flight > 0:
        return calibration_staircase(u0, r_space, wave_function, meson_1S, b_lower=b_lower,
            step_size = step_size/2, steps_taken = 0, flight = flight - 1)
    
    # Divergence has flipped and all layers have been run
    beta = (b_lower+b_upper)/2
    return (beta, step_size), scipy.integrate.odeint(wave_function, u0, r_space, args=(meson_1S, beta))


def calibrate_and_evaluate(u0, r_space, wave_function, meson_1S, initial_calibration_variable, step_size = 0.015, steps_taken = 0, flight = 5, energy_offset = 0.01):
    
    limit = 1
    offset = 0.01
    calibrated_variable_with_error = (initial_calibration_variable, 0)
    for _ in range(limit):
        calibrated_variable_with_error, numeric_solution = calibration_staircase(u0, r_space, wave_function, meson_1S, calibrated_variable_with_error[0], step_size, steps_taken, flight)
        u = numeric_solution[:,0]
        v = numeric_solution[:,1]

        
        nodes_tps  = nodes_turning_points(u, v, r_space)
        nodes = nodes_tps.pop('nodes')
        turning_points = nodes_tps.pop('turning_points')
        if turning_points['count'] < 3:
            pdf = wfns.square_wavefunction(u)
            pdf, u, v = wfns.normalise_wavefunction(r_space, pdf, u, v)
    
            return calibrated_variable_with_error, (pdf, u ,v), (nodes, turning_points)
        
        calibrated_variable_with_error[0] += offset
        
    else:
        pdf = wfns.square_wavefunction(u)
        pdf, u, v = wfns.normalise_wavefunction(r_space, pdf, u, v)
    
        return calibrated_variable_with_error, (pdf, u ,v), (nodes, turning_points)
    
cne = calibrate_and_evaluate

def polish_immortal(u0, r_space, wavefunction, meson_1S, b_lower_list, step_size = 0.015, steps_taken = 0, flight = 5):
    """
    Fills in a table of values of potential arguments that will later be evaluated for error |M_nl ref - M_nl numerical|
    The output is 2 lists of tuples. Each tuple is a set of arguments for the potential model (or it's error) 
    """
    
    candidate_beta_sets = []
    candidate_beta_errors_sets = []
    original_step_size = step_size
    # This method not yet using calibration mode
    for i in range(len(b_lower_list)):
        step_size = original_step_size
        while True:
            b_upper_list = [b for b in b_lower_list]
            b_upper_list[i] = b_upper_list[i] + step_size * (steps_taken+1)
            # b_upper_list is now the lower list with the 1 value at i being stepped once
            
            print(f"{b_lower_list= }")
            print(f"{b_upper_list= }")
            print('')
            v_lower = scipy.integrate.odeint(wavefunction, u0, r_space, args=(meson_1S, *b_lower_list))[:,1]
            v_upper = scipy.integrate.odeint(wavefunction, u0, r_space, args=(meson_1S, *b_upper_list))[:,1]

            
            divergence_has_flipped = (v_lower[-1] < 0) != (v_upper[-1] < 0)
            
            if not divergence_has_flipped:
                steps_taken += 1
                b_lower_list = b_upper_list
                
                calibrated_beta_list = b_lower_list
                calibrated_beta_list[i] += step_size/2
                beta_errors_list = [0]*len(calibrated_beta_list)
                beta_errors_list[i] = step_size
                candidate_beta_sets.append(tuple(calibrated_beta_list))
                candidate_beta_errors_sets.append(tuple(beta_errors_list))
                continue
                # return polish_immortal(u0, r_space, wavefunction, meson_1S, b_lower_list =b_upper_list,
                #     step_size= step_size, steps_taken= steps_taken+1, flight=flight)
            
            # print(layer)
            # Divergence has flipped
            if flight > 0:
                b_lower_list=b_lower_list
                step_size = step_size/2
                flight = flight - 1
                
                calibrated_beta_list = b_lower_list
                calibrated_beta_list[i] += step_size/2
                beta_errors_list = [0]*len(calibrated_beta_list)
                beta_errors_list[i] = step_size
                candidate_beta_sets.append(tuple(calibrated_beta_list))
                candidate_beta_errors_sets.append(tuple(beta_errors_list))
                continue
                # return polish_immortal(u0, r_space, wavefunction, meson_1S, b_lower_list=b_lower_list,
                #     step_size = step_size/2, steps_taken = 0, flight = flight - 1)
            
            # Divergence has flipped and all layers have been run
            calibrated_beta_list = b_lower_list
            calibrated_beta_list[i] += step_size/2
            beta_errors_list = [0]*len(calibrated_beta_list)
            beta_errors_list[i] = step_size
            
            candidate_beta_sets.append(tuple(calibrated_beta_list))
            candidate_beta_errors_sets.append(tuple(beta_errors_list))
            break


    return candidate_beta_sets, candidate_beta_errors_sets

def polish_evaluation(u0, r_space, wavefunction, meson_1S, initial_beta_list, step_size = 0.015, steps_taken = 0, flight = 5, energy_offset = 0.01):
    
    limit = 1
    offset = 0.01
    # calibrated_variable_with_error = (initial_calibration_variable, 0)
    beta_table, beta_errors_table = polish_immortal(u0, r_space, wavefunction, meson_1S, initial_beta_list, step_size, steps_taken, flight)
    return NotImplemented
    # for beta_set in beta_table:
    #     v_lower = scipy.integrate.odeint(wavefunction, u0, r_space, args=(meson_1S, *initial_beta_list))[:,1]
    #     u = numeric_solution[:,0]
    #     v = numeric_solution[:,1]

        
    #     nodes_tps  = nodes_turning_points(u, v, r_space)
    #     nodes = nodes_tps.pop('nodes')
    #     turning_points = nodes_tps.pop('turning_points')
    #     if turning_points['count'] < 3:
    #         pdf = wfns.square_wavefunction(u)
    #         pdf, u, v = wfns.normalise_wavefunction(r_space, pdf, u, v)
    
    #         return calibrated_variable_with_error, (pdf, u ,v), (nodes, turning_points)
        
    #     calibrated_variable_with_error[0] += offset
        
    # else:
    #     pdf = wfns.square_wavefunction(u)
    #     pdf, u, v = wfns.normalise_wavefunction(r_space, pdf, u, v)
    
    #     return calibrated_variable_with_error, (pdf, u ,v), (nodes, turning_points)


def energy_staircase(u0, r_space, calibrated_wave_function, meson, step_size = 0.015, steps_taken = 0, flight = 5):
    # Move epsilon, reduced mass, and fixed value into a tuple 
    # so other potentialls with differnt arguments can be used
    
    # This method not yet using calibration mode
    
    e_lower = meson.binding_energy
    e_upper = meson.binding_energy + step_size * (steps_taken+1)
    v_lower = scipy.integrate.odeint(calibrated_wave_function, u0, r_space, 
        args=(meson,))[:,1]
    
    meson.set_binding_energy(e_upper)
    v_upper = scipy.integrate.odeint(calibrated_wave_function, u0, r_space,
        args=(meson,))[:,1]
    divergence_has_flipped = (v_lower[-1] < 0) != (v_upper[-1] < 0)
    

    if not divergence_has_flipped:
        # Passes through the meson with it's new higher energy
        return energy_staircase(u0, r_space, calibrated_wave_function, meson,
            step_size= step_size, steps_taken= steps_taken+1, flight=flight)
    
    gamma = (e_lower+e_upper)/2
    # print(gamma)
    # print(layer)
    # Divergence has flipped
    if flight > 0:
        # takes a step back => meson is taken back to previous energy value
        # print("going to flight",flight )
        meson.set_binding_energy(e_lower)
        return energy_staircase(u0, r_space, calibrated_wave_function, meson,
            step_size = step_size/2, steps_taken = 0, flight = flight - 1)
    
    # Divergence has flipped and all layers have been run
    # Set meson to avarge of the bounding binding energies, e_lower and e_upper
    meson.set_binding_energy(gamma)
    # print(f"{meson.binding_energy= }")
    # print(f"{meson.mass =}")
    meson.binding_energy_error = step_size
    return meson, scipy.integrate.odeint(calibrated_wave_function, u0, r_space, args=(meson,))

def solve_for_energy(u0, r_space, wavefunction, meson, step_size = 0.015, steps_taken = 0, flight = 5):
    
    meson, numeric_solution, = energy_staircase(u0, r_space, wavefunction, meson, step_size, steps_taken, flight)
    u = numeric_solution[:,0]
    v = numeric_solution[:,1]

    
    nodes_tps  = nodes_turning_points(u, v, r_space)
    nodes = nodes_tps.pop('nodes')
    turning_points = nodes_tps.pop('turning_points')

    pdf = wfns.square_wavefunction(u)
    pdf, u, v = wfns.normalise_wavefunction(r_space, pdf, u, v)
    
    return meson, (pdf, u ,v), (nodes, turning_points)
