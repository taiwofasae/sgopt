from pydantic import BaseModel
from typing import Callable
from grinding.optimization.base import BaseOptimization, BaseOptimization7
from grinding.model.input_utils import GrindingInput, ProcessInput, ProcessInput7

class GeneticAlgorithm(BaseOptimization7):
    population : list[ProcessInput7] = None
    
    
    def run(self) -> ProcessInput7:
        print("Running Genetic algorithm...")
        
        # Get starting input set
        # Provide input range
        input_range = self.input_lower_bound.get_values(), self.input_upper_bound.get_values()
        # Provide objective function
        obj_fx = self.objective
        
        # Provide nonlinear constraint functions
        nonlcon_fx = self.constraints
        
        self.result = ProcessInput7(rough=GrindingInput(work_speed=5,cut_depth=.2, wheel_speed=40),
                                    finish=GrindingInput(work_speed=5,cut_depth=.2, wheel_speed=40),
                                    r_passes=5)
        
        return self.result