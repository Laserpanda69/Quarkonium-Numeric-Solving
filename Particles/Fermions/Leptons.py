from Fermion import Fermion

class Lepton(Fermion):
    def __init__(self, mass, spin, charge):
        super().__init__(mass, spin, charge)

class Neutrino(Lepton):
    NotImplemented()

class Electron(Lepton):
    NotImplemented()

class ElectronNeutrino(Neutrino):
    NotImplemented()

class Muon(Lepton):
    NotImplemented()

class MuonNeutrino(Neutrino):
    NotImplemented()

class Tauon(Lepton):
    NotImplemented()

class TauonNeutrino(Neutrino):
    NotImplemented()
    