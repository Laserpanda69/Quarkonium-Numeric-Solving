from Particles.Fermions.Quarks import Quark
from Particles.Particle import Particle
import regex as re
from numericalSolvers import energy_staircase

# Particles made of quarks
# held together by the strong force
# Can be either a Boson or a Fermion depending on quark Congig``
class Hadron(Particle):
    def __init__(self, state:tuple[int, int], *quarks):
        self.principle_number, self.angular_momentum_number= state
        self.quarks:list = quarks
        self.quark_mass:float = sum(q.mass for q in self.quarks)
        
        mass = None
        spin = sum(q.spin for q in self.quarks)
        charge = sum(q.charge for q in self.quarks)
        super().__init__(mass, spin, charge, state)
        
        self.reduced_mass = 1/sum(1/quark.mass for quark in self.quarks)
        
    def set_binding_energy(self, binding_energy: float):
        self.binding_energy = binding_energy
        self.mass = binding_energy + self.quark_mass
        
    def set_mass(self, mass: float):
        self.mass = mass
        self.binding_energy = mass - self.quark_mass
        
    def calculate_binding_energy(self, r_space, wave_function, beta, epsilon_lower):
        self, numeric_solution = energy_staircase([1,0], r_space, wave_function, self, beta, epsilon_lower)


