from pydantic import BaseModel

   
class CostParameters(BaseModel):
    M : float
    C_s : float
    C_w : float

class WorkpieceParameters(BaseModel):
    L_w : float
    b_w : float
    
class MachineParameters(BaseModel):
    R_t : float
    d_s : float
    b_s : float
    

class GrindingConfiguration(BaseModel):
    cost_parameters : CostParameters
    workpiece_parameters : WorkpieceParameters
    machine_parameters : MachineParameters
 