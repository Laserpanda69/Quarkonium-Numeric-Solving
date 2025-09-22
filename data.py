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
    ParticleName.UP:{
        'value': 2.16/1000,
        'error': 0.07/1000 #GeV
    },
    ParticleName.DOWN:{
        'value': 4.70,
        'error': 0.07/1000 #GeV
    },
    ParticleName.STRANGE:{
        'value': 3.49/1000,
        'error': 0.07/1000 #GeV
    },
    ParticleName.CHARM: {
        'value': 1.2730,
        'error': 0.0046 #GeV
        },
    ParticleName.BOTTOM: {
        'value': 4.183,#GeV
        'error': 0.007 #GeV
    },
    ParticleName.TOP:
        {
        'value': 172,
        'error': 0.31 #GeV
    },


    ParticleName.CHARMONIUM:{
        'reference':{
            1: {
                0:{
                    'value':2.9839,
                    'error': 0.4 #GeV
                    },
                },
            2:
            {
                0:{
                    'value':None,
                    'error': None #GeV
                },
                1:{
                    'value': None,
                    'error': None #GeV
                }
            }
        },
        
        'staircase':{}
    },
    
        ParticleName.BOTTOMONIUM:{
        'reference':{
            1: {
                0:{
                    'value':9.3987,
                    'error': 2.0/1000 #GeV
                    },
                },
            2:
            {
                0:{
                    'value':None,
                    'error': None #GeV
                },
                1:{
                    'value': None,
                    'error': None #GeV
                }
            }
        },
        'staircase':{}
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

