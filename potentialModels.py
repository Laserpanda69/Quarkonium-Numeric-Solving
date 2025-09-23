import math
import numpy as np
from data import ColorCharge, PhysicalConstants

ALPHA_S = PhysicalConstants.QCD_RUNNING_COUPLING_CONATANT.value
color_charge_count = len(ColorCharge)
CASIMIR_FACTOR = (color_charge_count**2-1)/(2*color_charge_count)
# CASIMIR_FACTOR = 4/3

print(f"QCD Runnning Constant = {ALPHA_S}")
print(f"Casimir Factor = {CASIMIR_FACTOR}")

# class PotentialModel():
#     def __init__(self, equation: callable, init_args: tuple):
#         self.equation = equation
#         self.args = init_args
        
#     def evaluate(self, r_space):
#         return self.equation(r_space)
    
#     def calbirate(self):
#         pass
    
# class CornellPotential(PotentialModel):
#     def __init__(self, qcd_string_tentsion):
#         equation = lambda r: -CASIMIR_FACTOR*ALPHA_S/r + qcd_string_tentsion*r
#         super().__init__(equation, qcd_string_tentsion)





def cornell_potential(r: float, qcd_string_tentsion: float) -> float:
    return -CASIMIR_FACTOR*ALPHA_S/r + qcd_string_tentsion*r

def calibrated_cornell_potential(beta: float) -> callable:
    return lambda r: cornell_potential(r, beta)


r_0_calc = lambda beta: np.power(CASIMIR_FACTOR*ALPHA_S, 0.5) * np.power(beta, -0.5)
r_1_calc = lambda beta: r_0_calc(beta) / math.e
r_2_calc = lambda beta: r_0_calc(beta) * math.e 
b_calc = lambda beta: beta * r_2_calc(beta)

bhanot_rudaz_head_calc  = lambda r: -CASIMIR_FACTOR*ALPHA_S/r
bhanot_rudaz_middle_calc = lambda b, r_0, r: b * math.log(r/r_0)
bhanot_rudaz_tail_calc   = lambda beta, r: beta * r


def bhanot_rudaz_potential(r: float, beta: float) -> float:
    if r < r_1_calc(beta):
        return bhanot_rudaz_head_calc(r)
    
    # now r >= r_1
    
    if r > r_2_calc(beta):
        return bhanot_rudaz_tail_calc(beta, r)
    
    # Now r_1 <= r < r_2
    r_0 = r_0_calc(beta)
    b   = b_calc(beta)
    return bhanot_rudaz_middle_calc(b, r_0, r)

def calibrated_bhanot_rudaz_potential(beta: float) -> callable:
    return lambda r: bhanot_rudaz_potential(r, beta)


def richardson_fulcher_potential(r: float, beta: float) -> float:
    meson_degrees_of_freedom = 3 # 1 orbit spin, 1 translation, 1 orbit distance 
    return beta*r - (8*math.pi)/((33-2*meson_degrees_of_freedom)*r)

def calibrated_richardson_fulcher_potential(beta: float) -> callable:
    return lambda r: richardson_fulcher_potential(r, beta)

def read_potential(r: float, beta:float, rho: float) -> float:
    r_0 = 13#GeV^(-1)
    # [rho] = unitless
    return -CASIMIR_FACTOR*ALPHA_S/r  +  beta*r*(1-np.exp(-(r/r_0)**rho))
# /(1+np.exp((r-13)))

def calibrate_potential_model(potential_model: callable, *args) -> callable:
    return lambda r: potential_model(r, *args)