import argparse

import json
import os
import sys
import time
import uuid

from grinding.model import common
from grinding.model.burn import BurnModel
from grinding.model.configuration import CostParameters, MachineParameters, ParametersLoad, ProcessParameters, WorkpieceParameters
from enum import Enum

from grinding.model.constraint import ProcessConstraint7
from grinding.model.grinding_model import GrindingModel7
from grinding.model.input_utils import GrindingInput, ProcessInput7
from grinding.model.surface_roughness import SurfaceRoughnessModel
from grinding.optimization.base import BaseOptimization7
from grinding.optimization.ga import GeneticAlgorithm
from grinding.optimization.gradient_descent import GradientDescent

# Define the parser
parser = argparse.ArgumentParser(description='SG Opt')

parser.add_argument('--title', '-t', action='store', dest='title', type=str,
                    default='run_opt', help='Title in output stream')

parser.add_argument('--verbose', '-v', action='store_true')

parser.add_argument('--parameter_json_path', action="store", dest='parameter_json_path', type=str, 
                    default='process_parameters.json', help='File path for process parameters')

class Optimizer(Enum):
    sgd = 'sgd'
    ga = 'ga'

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        try:
            return Optimizer[s]
        except KeyError:
            raise ValueError()
    
parser.add_argument('--optimizer', type=Optimizer.from_string, choices=list(Optimizer),
                    dest='optimizer', default='sgd', help="'sgd' or 'ga'")

parser.add_argument('--output_json_path', action="store", dest='output_json_path', 
                    default=None, help='File path for opt output')


parser.add_argument('--r_passes', action="store", dest='r_passes', 
                    default=None, help='No. of rough passes')

class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value
            
parser.add_argument('--pp', action=ParseKwargs, dest='pp', nargs='*',
                    help='Update parameters')

args = parser.parse_args()

output_json_file = args.output_json_path or str(uuid.uuid4())
output_json_file = output_json_file if os.path.splitext(output_json_file)[1] else f'{output_json_file}.json'

# Individual arguments can be accessed as attributes...
# print(args)
print('=========================')
print(f'Title: {args.title}')
print('=========================')

# Json file path
pp_json_path = args.parameter_json_path
pp_json_path = pp_json_path if os.path.splitext(pp_json_path)[1] else f'{pp_json_path}.json'

print('...loading process parameters')
pp = ParametersLoad.load_dict_from_file(pp_json_path)
# update parameters
if args.pp:
    pp = pp | args.pp

workpiece_params = WorkpieceParameters(**pp)
if args.verbose:
    print(workpiece_params)
cost_params = CostParameters(**pp)
if args.verbose:
    print(cost_params)
machine_params = MachineParameters(**pp)
if args.verbose:
    print(machine_params)
process_params = ProcessParameters(**pp)
if args.verbose:
    print(process_params)

print('...process parameters loading done!')

# Building grinding model
print('...Building grinding model...')

g_model = GrindingModel7(
        cost_params=cost_params,
        machine_params=machine_params,
        workpiece_params=workpiece_params,
        constraints=[
            ProcessConstraint7(desc='> Q_prime_l', fx= lambda x: process_params.Q_prime_l - common.qprime(x.rough)),
            ProcessConstraint7(desc='< Q_prime_u', fx= lambda x: common.qprime(x.rough) - process_params.Q_prime_u),
            ProcessConstraint7(desc='< Ra_max', 
                               fx= lambda x: SurfaceRoughnessModel(D_e=machine_params.D_e,
                                                                   f=machine_params.f,
                                                                   d=machine_params.d)(x.finish) - process_params.Ra_max),
            ProcessConstraint7(desc='no_burn_rough', 
                               fx= lambda x: BurnModel()(x.rough) - process_params.burnp_r_max),
            ProcessConstraint7(desc='no_burn_finish', 
                               fx= lambda x: BurnModel()(x.finish) - process_params.burnp_f_max),
            ProcessConstraint7(desc='= a total', fx= lambda x: abs(x.total_cut_depth - process_params.a_total) - 0.01)
        ],
        lower_input_range=GrindingInput(work_speed=process_params.v_w_l, cut_depth=process_params.a_l, wheel_speed=process_params.v_s_l),
        upper_input_range=GrindingInput(work_speed=process_params.v_w_u, cut_depth=process_params.a_u, wheel_speed=process_params.v_s_u),
    )

if args.verbose:
    print(g_model)
print('...Building optimization commands...')



g_opt_ga = GeneticAlgorithm(
    grinding_model=g_model,
    objective=g_model.total_cost,
    constraints=lambda x: [con.fx(x) for con in g_model.constraints],
    input_lower_bound=ProcessInput7.from_g_input(g_model.lower_input_range, r_passes=1),
    input_upper_bound=ProcessInput7.from_g_input(g_model.upper_input_range, r_passes=10)
)

if args.verbose:
    print(g_opt_ga)
    
print('...running...')
result = g_opt_ga.run()

if args.verbose:
    print("GA result:")
    print(result)
    
if args.optimizer == Optimizer.sgd:

    g_opt_sgd = GradientDescent(
        grinding_model=g_model,
        objective=g_model.total_cost,
        constraints=lambda x: [con.fx(x) for con in g_model.constraints],
        input_lower_bound=ProcessInput7.from_g_input(g_model.lower_input_range, r_passes=1),
        input_upper_bound=ProcessInput7.from_g_input(g_model.upper_input_range, r_passes=10)
    )

    if args.verbose:
        print(g_opt_sgd)


    result0 = result
    result = g_opt_sgd.run(start=result0)


print('Completed.\nResults:')
print(result)

# saving to file

with open(output_json_file, 'w') as f:
    f.write(result.to_json(population=g_opt_ga.population))
    
if args.optimizer == Optimizer.sgd:
    with open(output_json_file, 'w') as f:
        f.write(result.to_json(result0 = result0.to_json(),population=g_opt_ga.population))
    
with open(f"{os.path.splitext(output_json_file)[0]}.pp.json", 'w') as f:
    f.write(json.dumps(pp))
    
print('=========================')