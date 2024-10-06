from grinding.model.input import GrindingInput
from grinding.model.configuration import WorkpieceParameters, MachineParameters


class Time:
    def grinding(g_input: GrindingInput, 
                 workpiece_params: WorkpieceParameters) -> float:
        return workpiece_params.L_w / (1000. * g_input.work_speed)

    def rapid_traverse(machine_params : MachineParameters) -> float:
        return machine_params.R_t