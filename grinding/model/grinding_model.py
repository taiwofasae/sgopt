from grinding.model.power import PowerModel, PowerParameters
from pydantic import BaseModel
from typing import Callable, Tuple
from .input_utils import GrindingInput
from .input_utils import ProcessInput, ProcessInput7
from .configuration import CostParameters, MachineParameters, WorkpieceParameters
from .cost import CostModel
from .constraint import ProcessConstraint, ProcessConstraint7
from . import constants
from . import common
from .surface_roughness import SurfaceRoughnessModel
from .burn import BurnModel, CTLParameters

class GrindingModel(BaseModel):
    lower_input_range : GrindingInput
    upper_input_range : GrindingInput
    cost_params : CostParameters
    machine_params : MachineParameters
    workpiece_params : WorkpieceParameters
    cost_model : CostModel = None
    ctl_params : CTLParameters
    burn_model : BurnModel = None
    power_params : PowerParameters
    power_model : PowerModel = None
    constraints : list[ProcessConstraint] = []
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if not self.power_model:
            self.power_model = PowerModel(power_params=self.power_params,
                                          machine_params=self.machine_params)
            
        if not self.burn_model:
            self.burn_model = BurnModel(ctl_params=self.ctl_params,
                                        machine_params=self.machine_params,
                                        power_model=self.power_model)
        
        if not self.cost_model:
            self.cost_model = CostModel(cost_params=self.cost_params, 
                                        machine_params=self.machine_params, 
                                        workpiece_params=self.workpiece_params,
                                        burn_model=self.burn_model)
    
    def __str__(self) -> str:
        return '\n\t'.join(["GrindingModel:",
            f"Cost params: {self.cost_params}",
            f"Machine params: {self.machine_params}",
            f"Workpiece params: {self.workpiece_params}",
            f"Cost model: {self.cost_model}",
            f"Input ranges:",
            f"\tLower: {self.lower_input_range}",
            f"\tUpper: {self.upper_input_range}",
            f"Constraints:",
        ] + [f"\t{c}" for c in self.constraints])
    
    def grinding_cost(self, inputs : ProcessInput) -> float:
        return sum([self.cost_model.grinding(inp) for inp in inputs.inputs])
    
    def burn_cost(self, inputs : ProcessInput) -> float:
        return self.cost_model.burn(inputs)
    
    def total_cost(self, inputs : ProcessInput) -> float:
        return self.cost_model.total(inputs)
    
    def constraint_violations(self, inputs : ProcessInput) -> list[bool]:
        return [c(inputs) for c in self.constraints]

class GrindingModel7(GrindingModel):
    constraints : list[ProcessConstraint7] = []
    
    
if __name__ == '__main__':
    print(GrindingModel7(
        cost_params=CostParameters(M=200, C_s=200, C_w=0.25),
        machine_params=MachineParameters(R_t=0, d_s=250, b_s=25),
        workpiece_params=WorkpieceParameters(L_w=250, b_w=30),
        constraints=[
            ProcessConstraint7(desc='> Q_prime_l', fx= lambda x: common.qprime(x.rough) > constants.PROCESS_SETTINGS.Q_prime_l),
            ProcessConstraint7(desc='< Q_prime_u', fx= lambda x: common.qprime(x.rough) < constants.PROCESS_SETTINGS.Q_prime_u),
            ProcessConstraint7(desc='power_max', fx= lambda x: True),
            ProcessConstraint7(desc='force_max', fx= lambda x: True),
            ProcessConstraint7(desc='stress_max', fx= lambda x: True),
            ProcessConstraint7(desc='gratio_max', fx= lambda x: True),
            ProcessConstraint7(desc='cost_max', fx= lambda x: True),
            ProcessConstraint7(desc='wheelwear_max', fx= lambda x: True),
            ProcessConstraint7(desc='< Ra_max', 
                               fx= lambda x: SurfaceRoughnessModel(D_e=constants.MACHINE_PARAMETERS.D_e,
                                                                   f=constants.MACHINE_PARAMETERS.f,
                                                                   d=constants.MACHINE_PARAMETERS.d)(x.finish) < constants.PROCESS_SETTINGS.Ra_max),
            ProcessConstraint7(desc='no_burn_rough', 
                               fx= lambda x: BurnModel()(x.rough) < constants.PROCESS_SETTINGS.burn_rough_threshold),
            ProcessConstraint7(desc='no_burn_finish', 
                               fx= lambda x: BurnModel()(x.finish) < constants.PROCESS_SETTINGS.burn_finish_threshold),
            ProcessConstraint7(desc='= a total', fx= lambda x: (x.total_cut_depth - constants.PROCESS_SETTINGS.a_total) < 0.01)
        ],
        lower_input_range=GrindingInput(work_speed=40, cut_depth=0.05, wheel_speed=40),
        upper_input_range=GrindingInput(work_speed=40000, cut_depth=1.00, wheel_speed=70),
    ))