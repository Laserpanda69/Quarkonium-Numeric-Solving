from .Hadron import Hadron
from Particles.Bosons import Boson
from Particles.Fermions.Quarks import Quark

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
            assert(quark.is_anti_of(anti_quark))
        except:
            raise Exception(f"Quarkonia must be two quarks of like flavor/anti-flavor, not {type(quark)} and {type(anti_quark)}")
        Hadron.__init__(self, state, quark, anti_quark)
