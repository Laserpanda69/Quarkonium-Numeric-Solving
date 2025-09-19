import math
import numpy as np

ALPHA_S = 0.4


def cornell_potential(radii: list[float], alpha: float, beta: float) -> list[float]:
    return -(4/3)*alpha/radii + beta*radii


r_0_calc = lambda beta: np.power((4 * ALPHA_S / 2), 0.5) * np.power(beta, -0.5)
# np.power((4 * ALPHA_S / 2), 0.5) is a constant, so is pre-calculated to avoid dividing zero
# when ALPHA_S = 0.4
# R_0_ALPHA_COMPONENT = 0 if ALPHA_S == 0.4 else np.power((4 * ALPHA_S / 2), 0.5)
# r_0_calc = lambda beta:R_0_ALPHA_COMPONENT * np.power(beta, -0.5)
r_1_calc = lambda beta: r_0_calc(beta) / math.e
r_2_calc = lambda beta: r_0_calc(beta) * math.e
b_calc = lambda beta: beta * r_2_calc(beta)

bhanot_rudaz_head_calc  = lambda r: -(4/3) * (ALPHA_S / r)
bhanot_rudaz_middle_calc = lambda b, r_0, r: b * math.log(r_0/r)
bhanot_rudaz_tail_calc   = lambda beta, r: beta * r


def bhanot_rudaz_potential(r: float, beta: float) -> float:
    if r < r_1_calc(beta):
        return bhanot_rudaz_head_calc(r)
    
    # now r >= r_1
    
    if r >= r_2_calc(beta):
        return bhanot_rudaz_tail_calc(beta, r)
    
    # Now r_1 <= r < r_2
    r_0 = r_0_calc(beta)
    b   = b_calc(beta)
    return bhanot_rudaz_middle_calc(b, r_0, r)





# def bhanot_rudaz_potential(radii: list[float], alpha_s: float, beta: float) -> list[float]:
#     r_0 = r_0_calc(beta)
#     r_1 = r_1_calc(beta)
#     r_2 = r_2_calc(beta)
#     b   = b_calc(beta)
    
#     # This will get the index where r_n would be inserted, threfore eveything under it will be less
#     r_indexer = lambda r_n: bisect.bisect(radii, r_n) 
    
#     r_1_index = r_indexer(r_1)
#     r_2_index = r_indexer(r_2)
#     new_radii_head = [bhanot_rudaz_head_calc(r) for r in radii[:r_1_index]]
#     new_radii_middle = [bhanot_rudaz_middle_calc(b, r_0) for r in radii[r_1_index:r_2_index]]
#     new_radii_tail = [bhanot_rudaz_tail_calc(beta, r) for r in radii[r_2_index:]]
    
#     return [*[new_radii_head], *[new_radii_middle], *[new_radii_tail]]