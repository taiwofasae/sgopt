from typing import Any
from grinding.model.power import PowerModel
from pydantic import BaseModel

from grinding.model.configuration import MachineParameters
from .input_utils import GrindingInput, ProcessInput
import math

class CTLParameters(BaseModel):
    ctl_beta_0 : float
    ctl_beta_1 : float
    ctl_beta_2 : float
    
    def __str__(self) -> str:
        return "CTL Params: " + super().__str__()
    

class BurnModel(BaseModel):
    ctl_params : CTLParameters
    machine_params : MachineParameters
    power_model : PowerModel
    
    def _ctl_domain_fx(self, g_input : GrindingInput) -> float:
        return math.pow(self.machine_params.D_e, 0.25) * \
            math.pow(g_input.cut_depth, -0.75) * \
                math.pow(g_input.work_speed / 60.0, -0.5)
                
    def _ctl_line_fx(self, ctl : float, ec : float):
        f = self.ctl_params.ctl_beta_0 + \
            self.ctl_params.ctl_beta_1 * ctl + \
                self.ctl_params.ctl_beta_2 * ec
                
        logit = -f
        prob = 1. / (1 + math.exp(-logit))
        
        return logit, prob
    
    def ctl_line(self, g_input : GrindingInput) -> float:
        ctl = self._ctl_domain_fx(g_input)
        return self._ctl_line_fx(ctl=ctl, ec=self.power_model.specific_energy(g_input))
    
    def __call__(self, g_input : GrindingInput) -> float:
        return self.probability(g_input=g_input) > 0.5
    
    def probability(self, g_input : GrindingInput) -> float:
        logit, prob = self.ctl_line(g_input)
        return prob
    
    def process_probability(self, p_input : ProcessInput) -> float:
        return 1 - math.prod([1 - self.probability(inp) for inp in p_input.inputs])
    
    