# principle quantum number n
# angular momentum quantum numer l
# magnetic quantum number m or m_l
# electron spin quantum number m_s

class Particle():
    def __init__(self, mass: float, spin: float, charge: float, state: tuple[int, int], anti:float = 1, mass_error = 0):
        self.mass:float = mass
        self.spin:float = spin
        self.charge:float = charge*anti
        self.state = state
        self.mass_error:float = mass_error
        
        
    def is_anti_of(other_particle):
        return isinstance(other_particle, Particle)
    
    @staticmethod
    def convert_to_angular_momentum_letter(l: int) -> str:
        match l:
            case 1:
                L = 'S'
            case 2:
                L = 'P'
            case 3:
                L = 'D'
            case 4:
                L = 'F'
            case _:
                L = l + (ord('G') - 5)
                L = chr(L)
                
        return L


    @staticmethod
    def convert_to_angular_momentum_number(L: str) -> int:
        match L:
            case 'S':
                l = 1
            case 'P':
                l = 2
            case 'D':
                l = 3
            case 'F':
                l = 4
            case _:
                l = ord(L) - (ord('G') + 5)
                # raise Exception(f"{self.angular_momentum_number} out of range of know values of angular momentum")
        
        return l
    
    
    
    @staticmethod
    def convert_to_hydrogencic_state(self, spectroscopy_state: str) -> str:
        N = int(spectroscopy_state[0])
        l = self.convert_to_angular_momentum_number(spectroscopy_state[-1])
        n = N - l
        
        return n, l
    
    @staticmethod
    def convert_to_spectroscopy_state(self, n:int, l: int):
        N = n - l
        L = self.convert_to_angular_momentum_letter(l)
        return f"{N}{L}"
    
