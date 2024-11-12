from pydantic import BaseModel

from grinding.model.burn import BurnModel
from .input_utils import GrindingInput, ProcessInput
from .configuration import CostParameters, MachineParameters, WorkpieceParameters
from .time_utils import Time
from .wheel_wear import WhealWear


class CostModel(BaseModel):
    cost_params : CostParameters
    machine_params : MachineParameters
    workpiece_params : WorkpieceParameters
    burn_model : BurnModel
    
    def time(self, g_input : GrindingInput) -> float:
        return Time.grinding(g_input, self.workpiece_params) * self.cost_params.M / 60. + \
            Time.rapid_traverse(self.machine_params)
    
    def wheel_wear(self, g_input : GrindingInput) -> float:
        return WhealWear.grinding(g_input, self.workpiece_params) * self.cost_params.C_s

    def grinding(self, g_input : GrindingInput) -> float:
        return CostModel.time(self, g_input) + CostModel.wheel_wear(self, g_input)
    
    def burn(self, p_input : ProcessInput) -> float:
        return self.cost_params.C_w * self.burn_model.process_probability(p_input)
    
    def total(self, p_input : ProcessInput) -> float:
        return sum([CostModel.grinding(self, g_input) + CostModel.burn(self, p_input)
                for g_input in p_input.inputs])
    