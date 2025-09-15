import scipy.integrate 


def while_staircase_solver(u0, radii, wave_function, alpha, fixed_value, reduced_mass, epsilon, step_size = 0.015, flight = 5, calibration_mode = False):
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
        return while_staircase_solver(u0, radii, wave_function, alpha, fixed_value, reduced_mass, epsilon = epsilon_lower, step_size=step_size/2, flight= flight -1, calibration_mode=calibration_mode)
    
    args= (1,0,alpha,gamma, reduced_mass, fixed_value) if calibration_mode \
        else (1,0,alpha, fixed_value, reduced_mass, gamma)
    return gamma, scipy.integrate.odeint(wave_function, u0, radii, args= args)

# epsilon lower is given aqnd not calculated as it avoids calculating all values twice
def recursive_staircase_solver(u0, radii, wave_function, alpha, fixed_value, reduced_mass, epsilon_lower, step_size = 0.015, steps_taken = 0, flight = 5, calibration_mode = False):
    
    # Move epsilon, reduced mass, and fixed value into a tuple 
    # so other potentialls with differnt arguments can be used
    
    # This method not yet using calibration mode
    
    epsilon_upper = epsilon_lower + step_size * (steps_taken+1)
    v_lower = scipy.integrate.odeint(wave_function, u0, radii, args=(1,0,alpha, epsilon_lower, reduced_mass, fixed_value))[:,0]
    v_upper = scipy.integrate.odeint(wave_function, u0, radii, args=(1,0,alpha, epsilon_upper, reduced_mass, fixed_value))[:,0]
    
    divergence_has_flipped = (v_lower[-1] < 0) != (v_upper[-1] < 0)
    if not divergence_has_flipped:
        return recursive_staircase_solver(u0, radii, wave_function, alpha, fixed_value, reduced_mass, epsilon_lower =epsilon_upper,
            step_size= step_size, steps_taken= steps_taken+1, flight=flight)
    
    # print(layer)
    # Divergence has flipped
    if flight > 0:
        return recursive_staircase_solver(u0, radii, wave_function, alpha, fixed_value, reduced_mass, epsilon_lower=epsilon_lower,
            step_size = step_size/2, steps_taken = 0, flight = flight - 1)
    
    # Divergence has flipped and all layers have been run
    gamma = (epsilon_lower+epsilon_upper)/2
    return gamma, scipy.integrate.odeint(wave_function, u0, radii, args=(1,0,alpha,gamma, reduced_mass, fixed_value))


def calibration_staircase(u0, radii, wave_function, potential_arguments: tuple, b_lower, step_size = 0.015, steps_taken = 0, flight = 5):
    alpha, base_energy, reduced_mass = potential_arguments
    # Move epsilon, reduced mass, and fixed value into a tuple 
    # so other potentialls with differnt arguments can be used
    
    # This method not yet using calibration mode
    
    b_upper = b_lower + step_size * (steps_taken+1)
    v_lower = scipy.integrate.odeint(wave_function, u0, radii, args=(0,alpha, b_lower, reduced_mass, base_energy))[:,0]
    v_upper = scipy.integrate.odeint(wave_function, u0, radii, args=(0,alpha, b_upper, reduced_mass, base_energy))[:,0]
    
    divergence_has_flipped = (v_lower[-1] < 0) != (v_upper[-1] < 0)
    if not divergence_has_flipped:
        return calibration_staircase(u0, radii, wave_function, potential_arguments, b_lower =b_upper,
            step_size= step_size, steps_taken= steps_taken+1, flight=flight)
    
    # print(layer)
    # Divergence has flipped
    if flight > 0:
        return calibration_staircase(u0, radii, wave_function, potential_arguments, b_lower=b_lower,
            step_size = step_size/2, steps_taken = 0, flight = flight - 1)
    
    # Divergence has flipped and all layers have been run
    gamma = (b_lower+b_upper)/2
    return gamma, scipy.integrate.odeint(wave_function, u0, radii, args=(0,alpha,gamma, reduced_mass, base_energy))

def erergy_staircase(u0, radii, wave_function, potential_arguments: tuple, epsilon_lower, step_size = 0.015, steps_taken = 0, flight = 5):
    l, alpha, beta, reduced_mass = potential_arguments
    # Move epsilon, reduced mass, and fixed value into a tuple 
    # so other potentialls with differnt arguments can be used
    
    # This method not yet using calibration mode
    
    epsilon_upper = epsilon_lower + step_size * (steps_taken+1)
    v_lower = scipy.integrate.odeint(wave_function, u0, radii, args=(l,alpha, beta, reduced_mass, epsilon_lower))[:,0]
    v_upper = scipy.integrate.odeint(wave_function, u0, radii, args=(l,alpha, beta, reduced_mass, epsilon_upper))[:,0]
    
    divergence_has_flipped = (v_lower[-1] < 0) != (v_upper[-1] < 0)
    if not divergence_has_flipped:
        return erergy_staircase(u0, radii, wave_function, potential_arguments, epsilon_lower =epsilon_upper,
            step_size= step_size, steps_taken= steps_taken+1, flight=flight)
    
    gamma = (epsilon_lower+epsilon_upper)/2
    # print(gamma)
    # print(layer)
    # Divergence has flipped
    if flight > 0:
        # print("going to flight",flight )
        return erergy_staircase(u0, radii, wave_function, potential_arguments, epsilon_lower=epsilon_lower,
            step_size = step_size/2, steps_taken = 0, flight = flight - 1)
    
    # Divergence has flipped and all layers have been run
    return gamma, scipy.integrate.odeint(wave_function, u0, radii, args=(l,alpha,beta, reduced_mass, gamma))

