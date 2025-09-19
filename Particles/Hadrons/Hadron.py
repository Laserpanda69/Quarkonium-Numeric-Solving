from Fermions.Quarks import Quark

# Particles made of quarks
# held together by the strong force
class Hadron():
    def __innit__(self, quark_1: Quark, *additional_quarks):
        self.quarks = [quark_1, additional_quarks]

