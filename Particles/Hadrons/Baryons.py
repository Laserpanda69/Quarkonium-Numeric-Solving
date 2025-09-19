from Fermions.Quarks import Quark
from Hadron import Hadron
from Fermions import Fermion

# 3 quark particles
class Baryon(Hadron, Fermion):
    def __innit__(self, quark_1: Quark, quark_2: Quark, quark_3: Quark):
        return super().__innit__(quark_1, quark_2, quark_3)
    
class Proton(Baryon):
    NotImplemented()

class Neutron(Baryon):
    NotImplemented()