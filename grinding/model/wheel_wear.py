from grinding.model.input import GrindingInput
from grinding.model.configuration import WorkpieceParameters, MachineParameters
from grinding.model.grinding_ratio import GrindingRatio

class WhealWear:
    def grinding(g_input : GrindingInput,
                 workpiece_params : WorkpieceParameters) -> float:
        return GrindingRatio(workpiece_params=workpiece_params)(g_input)