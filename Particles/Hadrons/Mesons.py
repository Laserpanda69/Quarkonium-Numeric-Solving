from Hadron import Hadron
from Bosons import Boson
from Fermions.Quarks import Quark

# 2 quark particles
class Meson(Hadron, Boson):
    # Mesons are made of quark/anti_quark pairs
    def __innit__(self, quark: Quark, anit_quark: Quark):
        try:
            assert(anit_quark.color.value  * quark.color.value == 1)
        except:
            raise(f"Quarkonia must be two quarks of opposite color, not {anit_quark.color} and {quark.color}")
    
        self.quark = quark
        self.anti_quark = anit_quark
        super().__innit__(quark, anit_quark)


class Quarkonia(Meson):
    def __innit__(self, quark, anit_quark):
        super().__innit__(quark, anit_quark)
