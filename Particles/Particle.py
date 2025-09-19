class Particle():
    def __init__(self, mass: float, spin: float, charge: float):
        self.mass = mass
        self.spin = spin
        self.charge = charge
        
    def is_anti_of(other_particle):
        return isinstance(other_particle, Particle)