from enum import Enum
import scipy


# GeV
class ParticleNames(Enum):
    UP = "up"
    DOWN = "down"
    STRANGE = "strange"
    CHARM = "charm"
    TOP = "top"
    BOTTOM = "bottom"
    TRUTH = TOP
    BEAUTY = BOTTOM
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
    QCD_STRING_TENSTION = 0.18 #GeV^2_

# All masses in/converted to GeV for consistancy
particle_masses ={
    'unit': "GeV",
    ParticleNames.UP: 2.16/1000,#GeV +/-0.07 MeV
    ParticleNames.DOWN: 4.70/1000,#GeV+/-0.07 MeV
    ParticleNames.STRANGE: 3.49/1000,#GeV+/-0.07 MeV
    ParticleNames.CHARM: 1.2730,#+/-0.0046 GeV
    ParticleNames.TOP: 172,#+/- 0.31 GeV
    ParticleNames.BOTTOM: 4.183,#+/-0.007GeV

    ParticleNames.CHARMONIUM:{
        'experimental':{
            '1S': 2.9839
        },
        'staircase':{}
    }
}

particle_charges = {
    'unit': f"elementary charge e={scipy.e}",
    
    ParticleNames.UP: 2/3,
    ParticleNames.DOWN: -1/3,
    ParticleNames.STRANGE: -1/3,
    ParticleNames.CHARM: 2/3,
    ParticleNames.TOP: 2/3,
    ParticleNames.BOTTOM: -1/3,
}

