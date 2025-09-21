import numpy as np
import scipy.integrate 

import potentialModels as Vmods

def _wave_function(u0,r, l, beta, mu, E, potential):
    u,v= u0
    L = l*(l+1)
    potential = potential(r, beta)
    
    return [v,(L*u)/(r*r) -2*mu*u*(E-potential)]


def corenell_wave_function(u0,r, l, beta, mu, E):
    return _wave_function(u0,r, l, beta, mu, E, Vmods.cornell_potential)

        
def bhanot_rudaz_wave_function(u0,r, l, beta, mu, E):
    return _wave_function(u0,r, l, beta, mu, E, Vmods.bhanot_rudaz_potential)

def richerdson_fulcher_wave_function(u0,r, l, beta, mu, E):
    return _wave_function(u0,r, l, beta, mu, E, Vmods.richerdson_fulcher_potential)
        

        

def square_wavefunction(wave_function: list[float]) -> list[float]:
    pdf = np.zeros(wave_function.shape)
    for i in range(len(wave_function)):
        pdf[i] = abs(wave_function[i])**2
    return pdf

def normalise_wavefunction(
        r_space: list[float],
        probability_density_function: list[float], 
        wave_function: list[float], 
        differentiated_wave_function: list[float], 
    ) -> list[float]:
    
    norm = scipy.integrate.simpson(probability_density_function, r_space)
    recprical_norm = 1/norm
    root_reciprical_norm = 1/np.sqrt(norm)
    probability_density_function = probability_density_function*recprical_norm
    wave_function = wave_function*root_reciprical_norm
    differentiated_wave_function = differentiated_wave_function *root_reciprical_norm
    
    return probability_density_function, wave_function, differentiated_wave_function

def find_pdf_peaks(r_space, pdf, turning_points) -> list[float]:
        turning_point_indicies = np.searchsorted(r_space, turning_points)
        turning_point_indicies = np.clip(turning_point_indicies, 0, len(pdf) - 1)
        return list(pdf[turning_point_indicies])



