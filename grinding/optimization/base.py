from pydantic import BaseModel
from typing import Callable, Optional, Tuple
from grinding.model.grinding import GrindingModel
from grinding.model.input import GrindingInput
from grinding.model.input import ProcessInput, ProcessInput7, ProcessInput7Values

class BaseOptimization(BaseModel):
    grinding_model : GrindingModel
    objective : Callable[[ProcessInput], float]
    constraints : Callable[[ProcessInput], list[bool]]
    input_lower_bound : GrindingInput
    input_upper_bound : GrindingInput
    result : list[GrindingInput] = None
    
    def __str__(self) -> str:
        output = f"Optimization:\n" + \
            f"Grinding model: {self.grinding_model}\n" + \
                f"Objective: {self.objective}\n" + \
                    f"Constraints: {self.constraints}\n" + \
                        f"Lower bound: {self.input_lower_bound}\n" + \
                            f"Upper bound: {self.input_upper_bound}\n" + \
                                f"Results:\n" + \
                                    f"{self.result}"
                                    
        return output
        
    
        
    def convert_objective7_fx(input_fx : Callable[[ProcessInput], float]) -> Callable[[ProcessInput7Values], float]:
        return lambda x: input_fx(ProcessInput7.from_values(x))
    
    def objective7_fx(self, inputs: ProcessInput7Values) -> float:
        return self.objective(ProcessInput7.from_values(inputs))
    
    def run(self, start : GrindingInput | None) -> list[GrindingInput]:
        # Get starting input set
        # Provide input range
        input_range = self.input_lower_bound.get_values(), self.input_upper_bound.get_values()
        # Provide objective function
        obj_fx = BaseOptimization.convert_objective7_fx(self.objective)
        # Provide nonlinear constraint functions
        nonlcon_fx = self.constraints
        
        results = []
        
        self.result = results
        
        return self.result
    
    
if __name__ == '__main__':
    print(BaseOptimization())