
import json
from grinding.model import common, constants
from grinding.model.burn import BurnModel
from grinding.model.configuration import CostParameters, FileLoad, MachineParameters, WorkpieceParameters
from grinding.model.constraint import ProcessConstraint7
from grinding.model.grinding_model import GrindingModel, GrindingModel7
from grinding.model.input_utils import GrindingInput, ProcessInput, ProcessInput7
from grinding.model.surface_roughness import SurfaceRoughnessModel
from grinding.optimization.base import BaseOptimization, BaseOptimization7

g_model = GrindingModel7(
        cost_params=CostParameters(M=200, C_s=200, C_w=0.25),
        machine_params=MachineParameters(R_t=0, d_s=250, b_s=25),
        workpiece_params=WorkpieceParameters(L_w=250, b_w=30),
        constraints=[
            ProcessConstraint7(desc='> Q_prime_l', fx= lambda x: common.qprime(x.rough.work_speed) > constants.PROCESS_SETTINGS.Q_prime_l),
            ProcessConstraint7(desc='< Q_prime_u', fx= lambda x: common.qprime(x.rough.work_speed) < constants.PROCESS_SETTINGS.Q_prime_u),
            ProcessConstraint7(desc='power_max', fx= lambda x: True),
            ProcessConstraint7(desc='force_max', fx= lambda x: True),
            ProcessConstraint7(desc='stress_max', fx= lambda x: True),
            ProcessConstraint7(desc='gratio_max', fx= lambda x: True),
            ProcessConstraint7(desc='cost_max', fx= lambda x: True),
            ProcessConstraint7(desc='wheelwear_max', fx= lambda x: True),
            ProcessConstraint7(desc='< Ra_max', 
                               fx= lambda x: SurfaceRoughnessModel(D_e=constants.MACHINE_PARAMETERS.D_e,
                                                                   f=constants.MACHINE_PARAMETERS.f,
                                                                   d=constants.MACHINE_PARAMETERS.d)(x.finish) < constants.PROCESS_SETTINGS.Ra_max),
            ProcessConstraint7(desc='no_burn_rough', 
                               fx= lambda x: BurnModel()(x.rough) < constants.PROCESS_SETTINGS.burn_rough_threshold),
            ProcessConstraint7(desc='no_burn_finish', 
                               fx= lambda x: BurnModel()(x.finish) < constants.PROCESS_SETTINGS.burn_finish_threshold),
            ProcessConstraint7(desc='= a total', fx= lambda x: (x.total_cut_depth - constants.PROCESS_SETTINGS.a_total) < 0.01)
        ],
        lower_input_range=GrindingInput(work_speed=40, cut_depth=0.05, wheel_speed=40),
        upper_input_range=GrindingInput(work_speed=40000, cut_depth=1.00, wheel_speed=70),
    )

print(BaseOptimization7(
    grinding_model=g_model,
    objective=g_model.total_cost,
    constraints=lambda x: [con.fx(x) for con in g_model.constraints],
    input_lower_bound=ProcessInput7.from_g_input(g_model.lower_input_range, r_passes=1),
    input_upper_bound=ProcessInput7.from_g_input(g_model.upper_input_range, r_passes=10)
))

print(FileLoad.from_file('process_parameters.json', WorkpieceParameters))
print(FileLoad.from_file('process_parameters.json', CostParameters))

print(GrindingInput.from_json(GrindingInput(work_speed=4, cut_depth=2.3, wheel_speed=5.4).to_json()))
print(ProcessInput.from_json(ProcessInput(inputs=[
    GrindingInput(work_speed=4, cut_depth=2.3, wheel_speed=5.4),
    GrindingInput(work_speed=4, cut_depth=2.3, wheel_speed=5.4)
]).to_json()))

print(ProcessInput7.from_json(ProcessInput7(rough=GrindingInput(work_speed=4, cut_depth=2.3, wheel_speed=5.4),
    finish=GrindingInput(work_speed=4, cut_depth=2.3, wheel_speed=5.4),
    r_passes=4).to_json()))