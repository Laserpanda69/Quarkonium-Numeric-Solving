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


particle_masses ={
    ParticleNames.CHARM: 1.27,
    ParticleNames.CHARMONIUM:{
        '1S': 2.9839
    }
}