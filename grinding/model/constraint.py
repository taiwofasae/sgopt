from pydantic import BaseModel
from typing import Any, Callable
from .input_utils import GrindingInput
from .input_utils import ProcessInput, ProcessInput7

class Constraint(BaseModel):
    fx : Callable[[GrindingInput], Any]
    desc : str
    
    def __call__(self, g_input : GrindingInput) -> Any:
        return self.fx(g_input)
    
    def __str__(self) -> str:
        return '\n'.join([
            f"Constraint: {self.desc}: Callable[[GrindingInput], Any]"
        ])
    
class ProcessConstraint(BaseModel):
    fx : Callable[[ProcessInput], Any]
    desc : str
    
    def __call__(self, p_input : ProcessInput) -> Any:
        return self.fx(p_input)
    
    def __str__(self) -> str:
        return '\n'.join([
            f"Process constraint: {self.desc}: Callable[[ProcessInput], bool]"
        ])
        
class ProcessConstraint7(ProcessConstraint):
    fx : Callable[[ProcessInput7], Any]
    
    def __call__(self, p_input: ProcessInput7) -> Any:
        return self.fx(p_input)
    
    def __str__(self) -> str:
        return '\n'.join([
            f"Process constraint7: {self.desc}: Callable[[ProcessInput7], Any]"
        ])
    
if __name__ == '__main__':
    print(Constraint(
        desc='Ra',
        fx= lambda x: False
    ))
    print(ProcessConstraint(
        desc='Burn',
        fx=lambda x: True
    ))
    print(ProcessConstraint7(
        desc='RaBurn',
        fx=lambda x: True
    ))