from .Fermion import Fermion
from data import ParticleName, particle_charges, particle_masses, ColorCharge

# Strong force mediated Fermions
class Quark(Fermion):
    def __init__(self, mass, spin, charge, color):
        self.color:ColorCharge = color
        super().__init__ (mass, spin, charge)

# Light Quarks
class UpQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.UP], spin, particle_charges[ParticleName.UP], color)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiUpQuark)
    
class DownQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.DOWN], spin, particle_charges[ParticleName.DOWN], color)
    
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiDownQuark)
    
class StrangeQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.STRANGE], spin, particle_charges[ParticleName.STRANGE], color)
    
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiStrangeQuark)

# Heavy Quarks

class CharmQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.CHARM], spin, particle_charges[ParticleName.CHARM], color)
    
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiCharmQuark)

class BottomQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.BOTTOM], spin, particle_charges[ParticleName.BOTTOM], color)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiBottomQuark)
        

class TopQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.TOP], spin, particle_charges[ParticleName.TOP], color)

    def is_anti_of(self, quark: Quark):
        return isinstance(quark, AntiTopQuark)

# Anti-quarks

# Light Quarks
class AntiUpQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.UP], spin, -particle_charges[ParticleName.UP], color)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, UpQuark)   
    
    
class AntiDownQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.DOWN], spin, -particle_charges[ParticleName.DOWN], color)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, DownQuark)  


class AntiStrangeQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.STRANGE], spin, -particle_charges[ParticleName.STRANGE], color)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, StrangeQuark)
    
    
# Heavy Quarks
class AntiCharmQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.CHARM], spin, -particle_charges[ParticleName.CHARM], color)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, CharmQuark)

class AntiBottomQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.BOTTOM], spin, -particle_charges[ParticleName.BOTTOM], color)
        
    def is_anti_of(self, quark: Quark):
        return isinstance(quark, BottomQuark)        

class AntiTopQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleName.TOP], spin, -particle_charges[ParticleName.TOP], color)

    def is_anti_of(self, quark: Quark):
        return isinstance(quark, TopQuark)

