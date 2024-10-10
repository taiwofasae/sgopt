from pydantic import BaseModel
from typing import Callable
from grinding.optimization.base import BaseOptimization, BaseOptimization7
from grinding.model.input_utils import GrindingInput, ProcessInput, ProcessInput7

class GradientDescent(BaseOptimization7):
    
    
    
    def run(self, start : ProcessInput7) -> list[ProcessInput7]:
        print("Running Gradient descent...")
        
        # Get starting input set
        # Provide input range
        input_range = self.input_lower_bound.get_values(), self.input_upper_bound.get_values()
        # Provide objective function
        obj_fx = self.objective
        
        # Provide nonlinear constraint functions
        nonlcon_fx = self.constraints
        
        results = []
        
        self.result = results
        
        return self.result
    