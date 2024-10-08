from pydantic import BaseModel

   
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
    
    def __str__(self) -> str:
        return "Machine Params: " + super().__str__()
    

class GrindingConfiguration(BaseModel):
    cost_parameters : CostParameters
    workpiece_parameters : WorkpieceParameters
    machine_parameters : MachineParameters


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