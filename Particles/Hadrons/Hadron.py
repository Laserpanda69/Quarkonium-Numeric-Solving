from Particles.Fermions.Quarks import Quark
from Particles.Particle import Particle
import regex as re

# Particles made of quarks
# held together by the strong force
# Can be either a Boson or a Fermion depending on quark Congig
class Hadron(Particle):
    def __init__(self, state:str, *quarks):
        self.principle_number, self.angular_momentum_number= state
        
        if not re.match('\d',  self.angular_momentum_number):
            match self.angular_momentum_number.upper:
                case 'S':
                    self.angular_momentum_number = 1
                case 'P':
                    self.angular_momentum_number = 2
                case 'D':
                    self.angular_momentum_number = 3
                case 'F':
                    self.angular_momentum_number = 4
                case _:
                    raise Exception(f"{self.angular_momentum_number} out of range of know values of angular momentum")
        
        self.quarks = quarks
        self.quark_mass = sum(q.mass for q in self.quarks)
        
        mass = None
        spin = sum(q.spin for q in self.quarks)
        charge = sum(q.charge for q in self.quarks)
        super().__init__(mass, spin, charge)
        
    def set_binding_energy(self, binding_energy: float):
        self.binding_energy = binding_energy
        
    def set_mass(self, mass: float):
        self.mass = mass
        self.binding_energy = mass - self.quark_mass


