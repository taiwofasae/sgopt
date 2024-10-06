from pydantic import BaseModel
from grinding.model.input import GrindingInput
from grinding.model.configuration import WorkpieceParameters
from grinding.model.common import heq


class GrindingRatio(BaseModel):
    workpiece_params : WorkpieceParameters
    
    G_0 : float = 0
    g : float = 0
        
    
    def __call__(self, g_input : GrindingInput) -> float:
        return self.G_0 * pow(heq(g_input), self.g) 