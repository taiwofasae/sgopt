from pydantic import BaseModel
from typing import Callable
from grinding.optimization.base import BaseOptimization, BaseOptimization7
from grinding.model.input_utils import GrindingInput, ProcessInput, ProcessInput7, ProcessInput7Values
import pygad
from grinding.optimization import utils

num_generations = 50
num_parents_mating = 4

sol_per_pop = 8
num_genes = 7

init_range_low = 0
init_range_high = 1

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 20

class GeneticAlgorithm(BaseOptimization7):
    population : list[ProcessInput7] = None
    
    
    def rescale_solution_for_GA(self, solution, range_low : float = 0, range_high : float = 1) -> ProcessInput7:
        return utils._rescale_solution(solution, 
                                        source_lower_bound=self.input_lower_bound,
                                        source_upper_bound=self.input_upper_bound,
                                        lower_bound=ProcessInput7.from_scalar(range_low),
                                        upper_bound=ProcessInput7.from_scalar(range_high))
        
    def rescale_solution_from_GA(self, ga_solution : ProcessInput7Values) -> ProcessInput7:
        ga_solution = ProcessInput7.from_values(ga_solution)
        return utils._rescale_solution(ga_solution, 
                                        source_lower_bound=ProcessInput7.from_scalar(init_range_low), 
                                        source_upper_bound=ProcessInput7.from_scalar(init_range_high),
                                        lower_bound=self.input_lower_bound,
                                        upper_bound=self.input_upper_bound)
    
    
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
        
        
        def fitness_func(ga_instance, x, solution_idx):
            x = self.rescale_solution_from_GA(x)
            fitness = 1.0 / self.objective(x)
            return fitness
        
        
            
        
        lower_bound = self.rescale_solution_for_GA(self.input_lower_bound).get_values()
        upper_bound = self.rescale_solution_for_GA(self.input_upper_bound).get_values()
        
        ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_func,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=lower_bound,
                       init_range_high=upper_bound,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes,
                       gene_type=[float, float, float, int, float, float, float])
        
        #ga_instance.run()
        #self.population = [self.rescale_solution_from_GA(sol) for sol in ga_instance.population]
        self.population = [self.rescale_solution_from_GA(sol) for sol in ga_instance.initial_population]

        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        
        self.result = self.rescale_solution_from_GA(solution)
        
        return self.result