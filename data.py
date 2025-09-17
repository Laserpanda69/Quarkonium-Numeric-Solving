from enum import Enum
import math

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
        'experimental':{
            '1S': 2.9839
        },
        'numerical':{
            '1S': 0.0
        }
    }
}

physical_constants = {
    'strong_coupling_constant': 0.4,
    'e': math.e,
    'pi': math.pi
}