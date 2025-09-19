from Fermion import Fermion
from data import ParticleNames, particle_charges, particle_masses

# Strong force mediated Fermions
class Quark(Fermion):
    def __init__(self, spin, charge, color):
        self.color = color
        super().__init__ (spin, charge)

# Light Quarks
class UpQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.UP], spin, particle_charges[ParticleNames.UP], color)
        
    def is_anti_of(quark: Quark):
        return isinstance(quark, AntiUpQuark)
    
class DownQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.DOWN], spin, particle_charges[ParticleNames.DOWN], color)
    
    def is_anti_of(quark: Quark):
        return isinstance(quark, AntiDownQuark)
    
class StrangeQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.STRANGE], spin, particle_charges[ParticleNames.STRANGE], color)
    
    def is_anti_of(quark: Quark):
        return isinstance(quark, AntiStrangeQuark)

# Heavy Quarks

class CharmQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.CHARM], spin, particle_charges[ParticleNames.CHARM], color)
    
    def is_anti_of(quark: Quark):
        return isinstance(quark, AntiCharmQuark)

class BottomQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.BOTTOM], spin, particle_charges[ParticleNames.BOTTOM], color)
        
    def is_anti_of(quark: Quark):
        return isinstance(quark, AntiBottomQuark)
        

class TopQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.TOP], spin, particle_charges[ParticleNames.TOP], color)

    def is_anti_of(quark: Quark):
        return isinstance(quark, AntiTopQuark)

# Anti-quarks

# Light Quarks
class AntiUpQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.UP], spin, -particle_charges[ParticleNames.UP], color)
        
    def is_anti_of(quark: Quark):
        return isinstance(quark, UpQuark)   
    
    
class AntiDownQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.DOWN], spin, -particle_charges[ParticleNames.DOWN], color)
        
    def is_anti_of(quark: Quark):
        return isinstance(quark, DownQuark)  


class AntiStrangeQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.STRANGE], spin, -particle_charges[ParticleNames.STRANGE], color)
        
    def is_anti_of(quark: Quark):
        return isinstance(quark, StrangeQuark)
    
    
# Heavy Quarks
class AntiCharmQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.CHARM], spin, -particle_charges[ParticleNames.CHARM], color)
        
    def is_anti_of(quark: Quark):
        return isinstance(quark, CharmQuark)

class AntiBottomQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.BOTTOM], spin, -particle_charges[ParticleNames.BOTTOM], color)
        
    def is_anti_of(quark: Quark):
        return isinstance(quark, BottomQuark)        

class AntiTopQuark(Quark):
    def __init__(self, spin, color):
        super().__init__(particle_masses[ParticleNames.TOP], spin, -particle_charges[ParticleNames.TOP], color)

    def is_anti_of(quark: Quark):
        return isinstance(quark, TopQuark)

