from pydantic import BaseModel
from typing import Callable
from grinding.model.input import GrindingInput
from grinding.model.input import ProcessInput
from grinding.model.configuration import CostParameters, MachineParameters, WorkpieceParameters
from grinding.model.cost import CostModel

class GrindingModel(BaseModel):
    cost_params : CostParameters
    machine_params : MachineParameters
    workpiece_params : WorkpieceParameters
    cost_model : CostModel = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if not self.cost_model:
            self.cost_model = CostModel(self.cost_params, self.machine_params, self.workpiece_params)
    

    
    def grinding_cost(self, inputs : ProcessInput) -> float:
        return sum([self.cost_model.grinding(inp) for inp in inputs.inputs])
    
    def burn_cost(self, inputs : ProcessInput) -> float:
        return sum([self.cost_model.burn(inp) for inp in inputs.inputs])
    
    def total_cost(self, inputs : ProcessInput) -> float:
        return sum([self.cost_model.total(inp) for inp in inputs.inputs])
    
    def constraint_violations(self, inputs : ProcessInput) -> list[]
    