
##################################
####### Cornel Calibrating #######
##################################

print("Calibrating Cornell")
cornell_beta, sol, points_of_interest, error_on_cornell_beta = numericalSolvers.calibrate(
        U0, r_space, Wfns.corenell_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )

print(f"Cornell: {cornell_beta}")
        
##################################
######### BH Calibrating #########
##################################

print("Calibrating Bhnot Rudaz")
bh_beta, sol, points_of_interest, error_on_bh_beta = numericalSolvers.calibrate(
        U0, r_space, Wfns.bhanot_rudaz_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )

print(f"Bhnot Rudaz: {bh_beta}")


##################################
######### RF Calibrating #########
##################################

print("Calibrating Richardson Fulcher")
rf_beta, sol, points_of_interest, error_on_rf_beta = numericalSolvers.calibrate(
        U0, r_space, Wfns.richerdson_fulcher_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )

print(f"Richardson Fulcher: {rf_beta}")


##################################
######## Read Calibrating ########
##################################

print("Calibrating Read")
read_beta, sol, points_of_interest, error_on_read_beta = numericalSolvers.calibrate(
        U0, r_space, Wfns.read_wave_function, ground_state_meson,
        initial_calibration_variable = initial_calibration_variable, 
        flight = flights
    )

print(f"Read: {read_beta}")