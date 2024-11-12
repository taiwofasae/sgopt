
from typing import Callable
from grinding.model.input_utils import ProcessInput


def best_solution(sols : list[ProcessInput], 
                  minim_fx : Callable[[ProcessInput], float]) -> ProcessInput:
    return min(sols, key=lambda x: minim_fx(x))