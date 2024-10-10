from pydantic import BaseModel
from .input_utils import GrindingInput
from . import common

def actd(g_input : GrindingInput, D_e : float, f : float, d : float):
    qp = common.qprime(g_input)
    vw = g_input.work_speed
    a = g_input.cut_depth
    vs = g_input.wheel_speed
    
    return 4.9697 * (pow(d, 4/7) * pow(qp, 5/7)) / (pow(vs/60000, 1/7) * pow(D_e, 2/7) * pow(vs, 4/7) * pow(f, 0.83))

class SurfaceRoughnessModel(BaseModel):
    D_e : float
    f : float
    d : float
    
    def __call__(self, g_input : GrindingInput):
        act = actd(g_input, D_e=self.D_e, f=self.f, d=self.d)
        
        act1 = 0.460 * pow(act, 0.3)
        act2 = 0.789 * pow(act, 0.72)
        
        return act2 if act > 0.254 else act1
            