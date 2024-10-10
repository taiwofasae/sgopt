from .input_utils import GrindingInput
from .configuration import WorkpieceParameters, MachineParameters
from .grinding_ratio import GrindingRatio

class WhealWear:
    def grinding(g_input : GrindingInput,
                 workpiece_params : WorkpieceParameters) -> float:
        return GrindingRatio(workpiece_params=workpiece_params)(g_input)