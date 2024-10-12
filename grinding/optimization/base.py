from pydantic import BaseModel
from typing import Callable, Optional, Tuple
from ..model.grinding_model import GrindingModel, GrindingModel7
from ..model.input_utils import GrindingInput
from ..model.input_utils import ProcessInput, ProcessInput7, ProcessInput7Values, InputValues
from ..model.configuration import CostParameters, MachineParameters, WorkpieceParameters
from ..model.constraint import ProcessConstraint, ProcessConstraint7
from ..model.surface_roughness import SurfaceRoughnessModel
from ..model.burn import BurnModel
from ..model import constants, common

class BaseOptimization(BaseModel):
    grinding_model : GrindingModel
    objective : Callable[[ProcessInput], float]
    constraints : Callable[[ProcessInput], list[bool]]
    input_lower_bound : GrindingInput
    input_upper_bound : GrindingInput
    result : ProcessInput = None
    
    def __str__(self) -> str:
        return '\n'.join(["Optimization:",
                          f"Grinding model: {self.grinding_model}",
                          f"Objective: {self.objective.__name__}",
                          f"Constraints: {self.constraints}",
                          f"Lower bound: {self.input_lower_bound}",
                          f"Upper bound: {self.input_upper_bound}",
                          "Results:",
                          f"{self.result}"])
        
    def convert_objective_fx(input_fx : Callable[[ProcessInput], float]) -> Callable[[list[InputValues]], float]:
        return lambda x: input_fx(ProcessInput.from_values(x))
    
    def objective_fx(self, inputs: list[InputValues]) -> float:
        return self.objective(ProcessInput.from_values(inputs))
                                    
    
    def run(self, start : ProcessInput = None) -> list[ProcessInput]:
        print("Running BaseOptimization...")
        # Get starting input set
        # Provide input range
        input_range = self.input_lower_bound.get_values(), self.input_upper_bound.get_values()
        # Provide objective function
        obj_fx = self.objective
        
        # Provide nonlinear constraint functions
        nonlcon_fx = self.constraints
        
        results = []
        
        return self.result

class BaseOptimization7(BaseOptimization):
    
    objective : Callable[[ProcessInput7], float]
    constraints : Callable[[ProcessInput7], list[float]]
    input_lower_bound : ProcessInput7
    input_upper_bound : ProcessInput7
    result : list[ProcessInput7] = None
    
    def convert_objective7_fx(input_fx : Callable[[ProcessInput], float]) -> Callable[[ProcessInput7Values], float]:
        return lambda x: input_fx(ProcessInput7.from_values(x))
    
    def objective7_fx(self, inputs: ProcessInput7Values) -> float:
        return self.objective(ProcessInput7.from_values(inputs))
    
    def run(self, start : ProcessInput7 = None) -> list[ProcessInput7]:
        print("Running BaseOptimization7...")
        # Get starting input set
        # Provide input range
        input_range = self.input_lower_bound.get_values(), self.input_upper_bound.get_values()
        # Provide objective function
        obj_fx = self.objective
        
        # Provide nonlinear constraint functions
        nonlcon_fx = self.constraints
        
        results = []
        
        return self.result
    
if __name__ == '__main__':
    g_model = GrindingModel7(
        cost_params=CostParameters(M=200, C_s=200, C_w=0.25),
        machine_params=MachineParameters(R_t=0, d_s=250, b_s=25),
        workpiece_params=WorkpieceParameters(L_w=250, b_w=30),
        constraints=[
            ProcessConstraint7(desc='> Q_prime_l', fx= lambda x: common.qprime(x.rough.work_speed) > constants.PROCESS_SETTINGS.Q_prime_l),
            ProcessConstraint7(desc='< Q_prime_u', fx= lambda x: common.qprime(x.rough.work_speed) < constants.PROCESS_SETTINGS.Q_prime_u),
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
    )
    
    print(BaseOptimization7(
        grinding_model=g_model,
        constraints=g_model.constraints,
        input_lower_bound=ProcessInput7.from_g_input(g_model.lower_input_range, r_passes=1),
        input_upper_bound=ProcessInput7.from_g_input(g_model.upper_input_range, r_passes=10)
    ))