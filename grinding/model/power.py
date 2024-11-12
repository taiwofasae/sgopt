import math
from pydantic import BaseModel

from grinding.model import common
from grinding.model.configuration import MachineParameters
from grinding.model.input_utils import GrindingInput

class PowerParameters(BaseModel):
    P_0 : float
    r : float
    s : float
    
    def __str__(self) -> str:
        return "Power Params: " + super().__str__()

class PowerModel(BaseModel):
    power_params : PowerParameters
    machine_params : MachineParameters
    
    
    def _power_t(self, g_input : GrindingInput) -> float:
        qprime = common.qprime(g_input=g_input)
        heq = common.heq(g_input=g_input)
        P_0, r, s = self.power_params.P_0, self.power_params.r, self.power_params.s
        d_s = self.machine_params.d_s
        v_s = g_input.wheel_speed
        
        return self._power_t_fx(P_0, r, s, d_s, v_s, heq)
    
    def _power_t_fx(self, P_0, r, s, d_s, v_s, heq) -> float:
        
        return P_0 * math.pow(heq, r) * math.pow(d_s, s) * v_s
    
    def specific_energy(self, g_input : GrindingInput) -> float:
        qprime = common.qprime(g_input=g_input)
        return self._power_t(g_input=g_input) / qprime