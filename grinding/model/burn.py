from typing import Any
from pydantic import BaseModel
from input_utils import GrindingInput

class BurnModel(BaseModel):
    
    def __call__(self, g_input : GrindingInput) -> float:
        return 0.0