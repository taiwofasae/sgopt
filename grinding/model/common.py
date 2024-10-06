from grinding.model.input import GrindingInput

    
def heq(g_input : GrindingInput) -> float:
    return g_input.work_speed * g_input.cut_depth / g_input.wheel_speed