from pydantic import BaseModel
from .input_utils import GrindingInput
from .configuration import CostParameters, MachineParameters, WorkpieceParameters
from .time_utils import Time
from .wheel_wear import WhealWear


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
        return CostModel.time(self, g_input) + CostModel.wheel_wear(self, g_input)
    
    def burn(self, g_input : GrindingInput) -> float:
        return 0 # TODO
    
    def total(self, g_input : GrindingInput) -> float:
        return CostModel.grinding(self, g_input) + CostModel.burn(self, g_input)
    