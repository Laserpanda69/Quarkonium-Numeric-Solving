import numpy as np
import scipy.integrate 

import potentialModels as Vmods
# from Particles.Hadrons.Mesons import Meson

def _wave_function(u0,r, meson, potential_model, *potential_args):
    u,v= u0
    l = meson.state[1]
    L = l*(l+1)
    potential = potential_model(r, *potential_args)
    if not potential_args:
        # No potential_args => calibrated wavefunction
        potential = potential_model(r)
    
    return [v,(L*u)/(r*r) -2*meson.reduced_mass*u*(meson.binding_energy-potential)]


def cornell_wave_function(u0,r, meson, beta):
    return _wave_function(u0,r, meson, Vmods.cornell_potential, beta)


def bhanot_rudaz_wave_function(u0,r, meson, beta):
    return _wave_function(u0,r, meson, Vmods.bhanot_rudaz_potential, beta)

def richardson_fulcher_wave_function(u0,r, meson, beta):
    return _wave_function(u0,r, meson, Vmods.richardson_fulcher_potential, beta)
    

def read_wave_function(u0,r, meson, *args):
    return _wave_function(u0,r, meson, Vmods.read_potential, *args)


def calibrate_wavefunction(potential_model: callable, *args):
    if args:
        return lambda u0,r, meson: _wave_function(
            u0,r, meson,
            Vmods.calibrate_potential_model(potential_model, *args)
        )
    # potentail model is already calibrated
    return lambda u0,r, meson: _wave_function(
    u0,r, meson,
    potential_model
    )


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



