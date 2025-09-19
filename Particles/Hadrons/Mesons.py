from Hadron import Hadron
from Bosons import Boson
from Fermions.Quarks import Quark

# 2 quark particles
class Meson(Hadron, Boson):
    # Mesons are made of quark/anti_quark pairs
    def __innit__(self, quark: Quark, anit_quark: Quark):
        self.quark = quark
        self.anti_quark = anit_quark
        return super().__innit__(quark, anit_quark)

class Quarkonia(Meson):
    def __innit__(self, quark, anit_quark):
        return super().__innit__(quark, anit_quark)
    try:
        assert(anti_quark.flavor  == "anti-"+quark.flavor)
    except:
        raise(f"Quarkonia must be two quarks of opposite flavor, not {anti_quark.flavor} and {quark.flavor}")