from .Hadron import Hadron
from Particles.Bosons import Boson
from Particles.Fermions.Quarks import *
from data import ParticleName, particle_charges, particle_masses

GROUND_STATE = '1S'
REFERENCE = 'reference'
STAIRCASE = 'staircase'

# 2 quark particles

class Meson(Hadron):#, Boson):

    # Mesons are made of quark/anti_quark pairs
    def __int__(self, state, quark: Quark, anti_quark: Quark):
        try:
            assert(anti_quark.color.value  * 1/anti_quark.color.value == 1)
        except:
            raise Exception(f"Meson must be two quarks of opposite color, not {quark.color} and {anti_quark.color}")

        self.quark = quark
        self.anti_quark = anti_quark
        Hadron.__init__(self, state, quark, anti_quark)


class Quarkonia(Meson):
    def __init__(self, state, quark, anti_quark):
        
        try:
            assert(isinstance(quark, (CharmQuark, BottomQuark, TopQuark)))
        except:
            raise Exception(f"Quarkonia must be of heavy flavor, not {type(quark)= }")

        try:
            assert(isinstance(anti_quark, (AntiCharmQuark, AntiBottomQuark, AntiTopQuark)))
        except:
            raise Exception(f"Quarkonia must be of heavy flavor, {type(anti_quark)= }")

            
        try:
            assert(quark.is_anti_of(anti_quark))
        except:
            raise Exception(f"Quarkonia must be two quarks of like flavor/anti-flavor, not {type(quark)= } and {type(anti_quark)= }")
        Hadron.__init__(self, state, quark, anti_quark)
        
class Charmonium(Quarkonia):
    def __init__(self, state):
        super().__init__(state, CharmQuark(1/2, ColorCharge.RED), AntiCharmQuark(1/2, ColorCharge.RED))
        
        if state:
            self.set_mass(particle_masses[ParticleName.CHARMONIUM][REFERENCE][state[0]][state[1]]['value'])
            
class Bottomonium(Quarkonia):
    def __init__(self, state):
        super().__init__(state, BottomQuark(1/2, ColorCharge.RED), AntiBottomQuark(1/2, ColorCharge.RED))
        
        if state:
            self.set_mass(particle_masses[ParticleName.BOTTOMONIUM][REFERENCE][state[0]][state[1]]['value'])

            
class Toponium(Quarkonia):
    def __init__(self, state):
        super().__init__(state, TopQuark(1/2, ColorCharge.RED), AntiTopQuark(1/2, ColorCharge.RED))
        
        if state:
            self.set_mass(particle_masses[ParticleName.TOPONIUM][REFERENCE][state[0]][state[1]]['value'])