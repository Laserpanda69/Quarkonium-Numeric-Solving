from Particles.Particle import Particle

# Int spin +-1, +- 3
class Boson(Particle):
    def __init__():
        pass
    
    def __init__(self, mass, spin, charge):
        super().__init__(mass, spin, charge)
        try:
            assert((spin).is_integer)
        except:
            raise Exception(f"Bosons must have integer spin, not {spin}")



