from data import ParticleNames, particle_masses

class Particle():
    def __init__(self, mass: float, spin: float, charge: float):
        self.mass = mass,
        self.spin = spin,
        self.charge = charge
        
# Matter Particles. Half int spin +- 1/2, +-3/2
class Fermion(Particle):
    def __init__(self, mass, spin, charge):
        super().__init__(mass, spin, charge)
        try:
            assert((spin*2).is_integer)
        except:
            raise(f"Fermions must have half-integer spin, not {spin}")

# Force Carriers. Int spin +-1, +- 3
class Boson(Particle):
    def __init__(self, mass, spin, charge):
        super().__init__(mass, spin, charge)
        try:
            assert((spin).is_integer)
        except:
            raise(f"Bosons must have integer spin, not {spin}")


# Strong force mediated Fermions
class Quark(Fermion):
    def __init__(self, mass, spin, charge, color):
        super().__init__(mass, spin, charge, color)
    NotImplemented()

class UpQuark(Quark):
    NotImplemented()

class CharmQuark(Quark):
    NotImplemented()

class StrangeQuark(Quark):
    NotImplemented()

class TopQuark(Quark):
    NotImplemented()

class BottomQuark(Quark):
    NotImplemented()

# None strong force mediated particles
class Lepton(Fermion):
    def __init__(self, mass, spin, charge):
        super().__init__(mass, spin, charge)

class Neutrino(Fermion):
    NotImplemented()

class Electron(Lepton):
    NotImplemented()

class ElectronNeutrino(Lepton):
    NotImplemented()

class Muon(Lepton):
    NotImplemented()

class MuonNeutrino(Lepton):
    NotImplemented()

class Tauon(Lepton):
    NotImplemented()

class TauonNeutrino(Lepton):
    NotImplemented()


# Particles made of quarks
# held together by the strong force
class Hadron():
    def __innit__(self, quark_1: Quark, *additional_quarks):
        self.quarks = [quark_1, additional_quarks]


# 2 quark particles
class Meson(Hadron, Boson):
    # Mesons are made of quark/anti_quark pairs
    def __innit__(self, quark: Quark, anit_quark: Quark):
        return super().__innit__(quark, anit_quark)

# 3 quark particles
class Baryon(Hadron, Fermion):
    def __innit__(self, quark_1: Quark, quark_2: Quark, quark_3: Quark):
        return super().__innit__(quark_1, quark_2, quark_3)
    
class Proton(Baryon):
    NotImplemented()

class Neuton(Baryon):
    NotImplemented()