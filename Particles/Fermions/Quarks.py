from .Fermion import Fermion
from data import ParticleName, particle_charges, particle_masses, ColorCharge

# Strong force mediated Fermions
class Quark(Fermion):
    def __init__(self, mass, spin, charge, color, anti, mass_error = 0):
        self.color:ColorCharge = color
        super().__init__ (mass, spin, charge, anti, mass_error)

# Light Quarks
class UpQuark(Quark):
    def __init__(self, spin, color, anti = 1):
        super().__init__(particle_masses[ParticleName.UP]['value'], spin, 
            particle_charges[ParticleName.UP], color, anti)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiUpQuark)
    
class DownQuark(Quark):
    def __init__(self, spin, color, anti = 1):
        super().__init__(particle_masses[ParticleName.DOWN]['value'], spin, 
            particle_charges[ParticleName.DOWN], color, anti)
    
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiDownQuark)
    
class StrangeQuark(Quark):
    def __init__(self, spin, color, anti = 1):
        super().__init__(particle_masses[ParticleName.STRANGE]['value'], spin, 
            particle_charges[ParticleName.STRANGE], color, anti)
    
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiStrangeQuark)

# Heavy Quarks

class CharmQuark(Quark):
    def __init__(self, spin, color, anti = 1):
        super().__init__(particle_masses[ParticleName.CHARM]['value'], spin, 
            particle_charges[ParticleName.CHARM], color, anti, mass_error = particle_masses[ParticleName.CHARM]['error'])
    
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiCharmQuark)

class BottomQuark(Quark):
    def __init__(self, spin, color, anti = 1):
        super().__init__(particle_masses[ParticleName.BOTTOM]['value'], spin, 
            particle_charges[ParticleName.BOTTOM], color, anti)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiBottomQuark)
        

class TopQuark(Quark):
    def __init__(self, spin, color, anti = 1):
        super().__init__(particle_masses[ParticleName.TOP]['value'], spin, 
            particle_charges[ParticleName.TOP], color, anti)

    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiTopQuark)

# Anti-quarks

# Light Quarks
class AntiUpQuark(UpQuark):
    def __init__(self, spin, color):
        super().__init__(spin, color, anti = -1)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, UpQuark)   
    
    
class AntiDownQuark(DownQuark):
    def __init__(self, spin, color):
        super().__init__(spin, color, anti = -1)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, DownQuark)  


class AntiStrangeQuark(StrangeQuark):
    def __init__(self, spin, color):
        super().__init__(spin, color, anti = -1)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, StrangeQuark)
    
    
# Heavy Quarks
class AntiCharmQuark(CharmQuark):
    def __init__(self, spin, color):
        super().__init__(spin, color, anti = -1)

    def is_anti_of(self, quark: Quark):
        return isinstance(quark, CharmQuark)

class AntiBottomQuark(BottomQuark):
    def __init__(self, spin, color):
        super().__init__(spin, color, anti = -1)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, BottomQuark)        

class AntiTopQuark(TopQuark):
    def __init__(self, spin, color):
        super().__init__(spin, color, anti = -1)

    def is_anti_of(self, quark: Quark):
        return isinstance(quark, TopQuark)

