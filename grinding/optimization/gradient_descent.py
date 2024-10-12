from pydantic import BaseModel
from typing import Callable
from grinding.model import solutions_utils
from grinding.optimization.base import BaseOptimization, BaseOptimization7
from grinding.model.input_utils import GrindingInput, ProcessInput, ProcessInput7, ProcessInput7Values
from scipy.optimize import minimize, Bounds, LinearConstraint, NonlinearConstraint
import numpy as np


class GradientDescent(BaseOptimization7):
    result : ProcessInput7 = None
    
    
    def run(self, start : ProcessInput7) -> ProcessInput7:
        print("Running Gradient descent algorithm...")
        
        # Get starting input set
        ilb = self.input_lower_bound
        iub = self.input_upper_bound

        # Provide input range
        bounds = Bounds(np.array(ilb.get_float_values()), 
                        np.array(iub.get_float_values()))
        
        
        linear_constraint = LinearConstraint([[1, 1, 1, 1, 1, 1]], 
                                             -np.inf, np.inf)
        
        solutions = []
        
        for r_passes in range(ilb.r_passes, iub.r_passes+1):
            
        
            # Provide nonlinear constraint functions
            nonlcon_fx = lambda x: np.array(self.constraints(ProcessInput7.from_float_values(x, r_passes)))
            nonlinear_constraint = NonlinearConstraint(nonlcon_fx, -np.inf, 0)
            
            # Provide objective function
            obj_fx = lambda x: np.array(self.objective(ProcessInput7.from_float_values(x, r_passes)))
            
            
            
            res = minimize(obj_fx, start.get_float_values(), method='trust-constr',
                constraints=[linear_constraint, nonlinear_constraint],
                options={'verbose': 1}, bounds=bounds)
            
            solutions.append(ProcessInput7.from_float_values(res.x, r_passes))
            
        self.result = solutions_utils.best_solution(solutions, self.objective)
        
        return self.result
    