from .input_utils import GrindingInput

    
def heq(g_input : GrindingInput) -> float:
    return g_input.work_speed * g_input.cut_depth / g_input.wheel_speed

def qprime(g_input : GrindingInput) -> float:
    return g_input.work_speed * g_input.cut_depth / 60


