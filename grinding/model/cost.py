from pydantic import BaseModel
from grinding.model.input import GrindingInput
from grinding.model.configuration import CostParameters, MachineParameters, WorkpieceParameters
from grinding.model.time import Time
from grinding.model.wheel_wear import WhealWear


class CostModel(BaseModel):
    cost_params : CostParameters
    machine_params : MachineParameters
    workpiece_params : WorkpieceParameters
    
    def time(self, g_input : GrindingInput) -> float:
        return Time.grinding(g_input, self.workpiece_params) * self.cost_params.M / 60. + \
            Time.rapid_traverse(self.machine_params)
    
    def wheel_wear(self, g_input : GrindingInput) -> float:
        return WhealWear.grinding(g_input, self.workpiece_params) * self.cost_params.C_s

    def grinding(self, g_input : GrindingInput) -> float:
        return CostModel.time(g_input) + CostModel.wheel_wear(g_input)
    
    def burn(self, g_input : GrindingInput) -> float:
        return 0
    
    def total(self, g_input : GrindingInput) -> float:
        return CostModel.grinding(g_input) + CostModel.burn(g_input)
    