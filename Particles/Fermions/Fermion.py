from Particles.Particle import Particle

# Matter Particles. Half int spin +- 1/2, +-3/2
class Fermion(Particle):
    def __init__(self, mass, spin, charge):
        super().__init__(mass, spin, charge)
        try:
            assert((spin*2).is_integer)
        except:
            raise(f"Fermions must have half-integer spin, not {spin}")
        
        # None strong force mediated particles

