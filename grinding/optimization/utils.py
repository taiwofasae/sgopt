from grinding.model.input_utils import ProcessInput7


def _rescale_solution(source_soln : ProcessInput7, 
                              source_lower_bound : ProcessInput7, source_upper_bound : ProcessInput7,
                              lower_bound : ProcessInput7, upper_bound : ProcessInput7) -> ProcessInput7:
            
            diff = source_upper_bound - source_lower_bound
            diff.r_passes = 1
            target_soln = (source_soln - source_lower_bound) / diff
            target_soln = target_soln * (upper_bound - lower_bound) + lower_bound
            target_soln.r_passes = source_soln.r_passes
            
            return ProcessInput7(rough=target_soln.rough, finish=target_soln.finish,
                                 r_passes=target_soln.r_passes)