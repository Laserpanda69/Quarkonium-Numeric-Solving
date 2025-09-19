from enum import Enum

# GeV
class ParticleNames(Enum):
    UP = "up"
    DOWN = "down"
    CHARM = "charm"
    STRANGE = "strange"
    TOP = "top"
    BOTTOM = "bottom"
    UPONIUM = "uponium"
    DOWNONIUM = "downonium"
    CHARMONIUM = "charmonium"
    STRANGEONIUM = "strangeonium"
    TOPONIUM = "toponium"
    BOTTOMONIUM = "bottomonium"
    
class ColorCharges(Enum):
    RED = 2
    GREEN = 3
    BLUE = 4

class PhysicalConstants(Enum):
    QCD_RUNNING_COUPLING_CONATANT = 0.4
    QCD_STRING_TENSTION = 0.18 #GeV^2


particle_masses ={
    ParticleNames.CHARM: 1.27,
    ParticleNames.CHARMONIUM:{
        'experimental':{
            '1S': 2.9839
        },
        'staircase':{}
    }
}

