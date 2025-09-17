import numpy as np
import scipy.integrate 

import potentialModels

from typing import Callable

def _wave_function(u0,r, l, mu, E, potential_model: Callable, potential_arguments: tuple):
    u,v= u0
    L = l*(l+1)
    potential = potential_model(*potential_arguments)
        
    
    return [v,(L*u)/(r*r) -2*mu*u*(E-potential)]

def corenell_wave_function(u0,r, l, alpha, beta, mu, E):
    return _wave_function(u0,r, l, mu, E, potentialModels.cornell_potential, (r, alpha, beta))
        


def square_wavefunction(wave_function: list[float]) -> list[float]:
    pdf = np.zeros(wave_function.shape)
    for i in range(len(wave_function)):
        pdf[i] = abs(wave_function[i])**2
    return pdf

def normalise_wavefunction(
        probability_density_function: list[float], 
        wave_function: list[float], 
        v: list[float], 
        radii: list[float]
    ) -> list[float]:
    
    norm = scipy.integrate.simpson(probability_density_function, radii)
    recprical_norm = 1/norm
    root_reciprical_norm = 1/np.sqrt(norm)
    probability_density_function = probability_density_function*recprical_norm
    wave_function = wave_function*root_reciprical_norm
    v = v *root_reciprical_norm
    
    return probability_density_function, wave_function, v
