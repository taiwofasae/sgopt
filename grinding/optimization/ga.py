from pydantic import BaseModel
from typing import Callable
from grinding.optimization.base import BaseOptimization, BaseOptimization7
from grinding.model.input_utils import GrindingInput, ProcessInput, ProcessInput7
import pygad

num_generations = 50
num_parents_mating = 4

sol_per_pop = 8
num_genes = 7

init_range_low = -2
init_range_high = 5

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10

class GeneticAlgorithm(BaseOptimization7):
    population : list[ProcessInput7] = None
    
    
    
    
    def run(self, r_passes = None) -> ProcessInput7:
        print("Running Genetic algorithm...")
        
        # Get starting input set
        # Provide input range
        input_range = self.input_lower_bound.get_values(), self.input_upper_bound.get_values()
        # Provide objective function
        obj_fx = self.objective
        
        # Provide nonlinear constraint functions
        nonlcon_fx = self.constraints
        
        self.population = []
        
        self.result = ProcessInput7.from_values([800, 0.5, 50, 4, 700, 0.5, 60])
        return self.result
        
        def fitness_func(ga_instance, x, solution_idx):
            fitness = 1.0 / self.objective(ProcessInput7.from_values(x))
            return fitness
        
        ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_func,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes)
        
        ga_instance.run()
        
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        
        self.result = ProcessInput7(rough=GrindingInput(work_speed=5,cut_depth=.2, wheel_speed=40),
                                    finish=GrindingInput(work_speed=5,cut_depth=.2, wheel_speed=40),
                                    r_passes=5)
        
        return self.result