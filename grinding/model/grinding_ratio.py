from pydantic import BaseModel
from input_utils import GrindingInput
from configuration import WorkpieceParameters
from common import heq


class GrindingRatio(BaseModel):
    G_0 : float = 0
    g : float = 0
        
    def __str__(self) -> str:
        return "Grinding ratio: " + super().__str__()
    
    def __call__(self, g_input : GrindingInput) -> float:
        return self.G_0 * pow(heq(g_input), self.g) 
    

if __name__ == "__main__":
    print(GrindingRatio(g=23,G_0=1000))