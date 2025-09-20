from enum import Enum
import scipy


# GeV
class ParticleName(Enum):
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
    
class ColorCharge(Enum):
    RED = 2
    GREEN = 3
    BLUE = 4
    


class PhysicalConstants(Enum):
    QCD_RUNNING_COUPLING_CONATANT = 0.4
    QCD_STRING_TENSTION = 0.18 #GeV^2_

# All masses in/converted to GeV for consistancy
particle_masses ={
    'unit': "GeV",
    ParticleName.UP: 2.16/1000,#GeV +/-0.07 MeV
    ParticleName.DOWN: 4.70/1000,#GeV+/-0.07 MeV
    ParticleName.STRANGE: 3.49/1000,#GeV+/-0.07 MeV
    ParticleName.CHARM: 1.2730,#+/-0.0046 GeV
    ParticleName.TOP: 172,#+/- 0.31 GeV
    ParticleName.BOTTOM: 4.183,#+/-0.007GeV

    ParticleName.CHARMONIUM:{
        'reference':{
            '1S': 2.9839#GeV
        },
        'staircase':{}
    },
    
    ParticleName.BOTTOMONIUM:{
        'reference':{
            '1S': 9.3987#Gev +/- 2.0MeV
        }
        
    }
}

particle_charges = {
    'unit': f"elementary charge e={scipy.constants.e}",
    
    ParticleName.UP: 2/3,
    ParticleName.DOWN: -1/3,
    ParticleName.STRANGE: -1/3,
    ParticleName.CHARM: 2/3,
    ParticleName.TOP: 2/3,
    ParticleName.BOTTOM: -1/3,
}

