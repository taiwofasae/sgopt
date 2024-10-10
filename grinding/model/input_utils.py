from pydantic import BaseModel, computed_field
from typing import Tuple, Optional
import json

ProcessInput7Values = Tuple[float, float, float, int, float, float, float]
InputValues = Tuple[float, float, float]

class GrindingInput(BaseModel):
    work_speed : float
    cut_depth : float
    wheel_speed : float
    
    def get_values(self) -> InputValues:
        return [self.work_speed, self.cut_depth, self.wheel_speed]
    
    def from_values(values : InputValues):
        return GrindingInput(work_speed=values[0], cut_depth=values[1], wheel_speed=values[2])
    
    def to_json(self) -> str:
        return f'{{"work_speed":{self.work_speed}, "cut_depth": {self.cut_depth}, "wheel_speed": {self.wheel_speed}}}'
    
    def from_json(string : str):
        data = json.loads(string)
        return GrindingInput(**data)
    
    

class ProcessInput(BaseModel):
    inputs : list[GrindingInput]
    
    @computed_field
    @property
    def n_passes(self) -> int:
        return len(self.inputs)
    
    @computed_field
    @property
    def total_cut_depth(self) -> float:
        return sum([inp.cut_depth for inp in self.inputs])
    
    def __str__(self) -> str:
        output = f"Process Input:\n"
        output += f"Total cut depth: {self.total_cut_depth}\t No. of passes: {self.n_passes}\n"
        output += '\n'.join([f"{i+1}: {inp}" for i,inp in zip(range(len(self.inputs)), self.inputs)])
        return output
    
    def get_values(self) -> list[InputValues]:
        return [x.get_values() for x in self.inputs]
    
    def from_values(values : list[InputValues]):
        return ProcessInput(inputs=[GrindingInput.from_values(val) for val in values])
    
    def to_json(self) -> str:
        return '{"inputs":[' + ',\n\t'.join([inp.to_json() for inp in self.inputs]) + ']}'
    
    def from_json(string : str):
        data = json.loads(string)
        return ProcessInput(**data)


class ProcessInput7(ProcessInput):
    rough : GrindingInput
    finish : GrindingInput
    r_passes : int
    
    def __init__(self, **kwargs):
        super().__init__(inputs=[kwargs['rough']]*kwargs['r_passes'] + [kwargs['finish']], **kwargs)
    
    def __str__(self) -> str:
        output = f"Process 7 Inputs:\n"
        output += f"Total cut depth: {self.total_cut_depth}\t No. of passes: {self.n_passes}\n"
        output += f"{self.r_passes}x Rough: {self.rough}\n"
        output += f"Finish  : {self.finish}\n"
        return output
    
    def get_values(self) -> ProcessInput7Values:
        return self.rough.get_values() + [self.r_passes] + [self.finish.get_values()]
    
    def from_values(values : ProcessInput7Values):
        return ProcessInput7(rough=values[:3], r_passes=values[3], finish=values[4:])
    
    def from_g_input(g_input : GrindingInput, r_passes : int):
        return ProcessInput7(rough=g_input, finish=g_input, r_passes=r_passes)
    
    def to_json(self) -> str:
        return f'{{"rough":{self.rough.to_json()}, "r_passes": {self.r_passes}, "finish": {self.finish.to_json()}}}'
    
    def from_json(string : str):
        data = json.loads(string)
        return ProcessInput7(**data)
    
    
    
if __name__ == '__main__':
    print(GrindingInput(work_speed=34, wheel_speed=50, cut_depth=0.03))
    print(ProcessInput(inputs=[GrindingInput(work_speed=34, wheel_speed=50, cut_depth=0.03), GrindingInput(work_speed=34, wheel_speed=50, cut_depth=0.03)],
                       total_cut_depth=3.5))
    print(ProcessInput7(rough=GrindingInput(work_speed=34, wheel_speed=50, cut_depth=0.03), finish=GrindingInput(work_speed=40, wheel_speed=20, cut_depth=0.07), r_passes=4))