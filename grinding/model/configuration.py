from pydantic import BaseModel
from typing import Tuple, TypeVar, Generic
import json

   
class CostParameters(BaseModel):
    M : float
    C_s : float
    C_w : float
    
    def __str__(self) -> str:
        return "Cost Params: " + super().__str__()

class WorkpieceParameters(BaseModel):
    L_w : float
    b_w : float
    
    def __str__(self) -> str:
        return "Workpiece Params: " + super().__str__()
    
class MachineParameters(BaseModel):
    R_t : float
    d_s : float
    b_s : float
    D_e : float
    f : float
    d : float
    
    def __str__(self) -> str:
        return "Machine Params: " + super().__str__()
    

class ProcessParameters(BaseModel):
    Q_prime_l : float
    Q_prime_u : float
    Ra_max : float
    burnp_r_max : float
    burnp_f_max : float
    a_total : float
    v_w_l : float
    v_w_u : float
    a_l : float
    a_u : float
    v_s_l : float
    v_s_u : float
    
    def __str__(self) -> str:
        return "Process Params: " + super().__str__()

class GrindingConfiguration(BaseModel):
    cost_parameters : CostParameters
    workpiece_parameters : WorkpieceParameters
    machine_parameters : MachineParameters

T = TypeVar
class ParametersLoad:
    def load_dict_from_file(filepath : str) -> dict:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        return dict(**data)
        
    def from_file(filepath : str, parameterType : T) -> T:
        
        kv = ParametersLoad.load_dict_from_file(filepath)
        return parameterType(**kv)

if __name__ == '__main__':
    print(CostParameters(
        M=200,
        C_s=0.25,
        C_w=200
    ))
    print(WorkpieceParameters(
        L_w=250,
        b_w=25
    ))
    print(MachineParameters(
        R_t=25,
        d_s=350,
        b_s=35
    ))
    print(GrindingConfiguration(
        cost_parameters=CostParameters(M=200, C_s=0.25,C_w=200),
        workpiece_parameters=WorkpieceParameters(L_w=250, b_w=25),
        machine_parameters=MachineParameters(R_t=23, d_s=300, b_s=40)
    ))