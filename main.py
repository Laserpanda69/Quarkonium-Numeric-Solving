import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate 

def cornell_potential(radii: list[float], alpha: float, beta: float) -> list[float]:
    return -(4/3)*alpha/radii + beta*2

def wave_function(U0,r, n, l, alpha, beta, mu, E):
    u,v= U0
    a = l*(l+1)
    b = 2*mu*E
    c = 2*mu*alpha
    d = 2*mu*beta
    
    potential = cornell_potential(r, alpha, beta)
    
    return [v,(a/r**2)*u -2*mu*(E-potential)]

def square_wavefunction(wave_function: list[float]) -> list[float]:
    pdf = np.zeros(wave_function.shape)
    for i in range(len(wave_function)):
        pdf[i] = abs(wave_function[i])**2
    return pdf
def normalise_wavefunction(
        probability_density_function: list[float], 
        wave_function: list[float], 
        potential: list[float], 
        radii: list[float]
    ) -> list[float]:
    
    norm = scipy.integrate.simpson(probability_density_function, radii, even='first')
    recprical_norm = 1/norm
    root_reciprical_norm = 1/np.sqrt(norm)
    probability_density_function = probability_density_function*recprical_norm
    wave_function = wave_function*root_reciprical_norm
    potential = potential *root_reciprical_norm
    
    return probability_density_function, wave_function, potential


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
beta = 0.195
charm_quark_mass = 1.34
charmonium_mass_1S = 3.068
charmonium_energy_1S = charmonium_mass_1S - 2*charm_quark_mass
#mu = mc/2

recpricol_mu = 1/charm_quark_mass + 1/charm_quark_mass
mu = 1/recpricol_mu
r = np.linspace(0.0000001, 6, 10000)

sol = scipy.integrate.odeint(wave_function, U0, r, args=(1,0,alpha,beta, mu, charmonium_energy_1S))
plt.plot(r, sol[:,0])
plt.show()