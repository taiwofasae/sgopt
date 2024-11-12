from pydantic import BaseModel, computed_field
from typing import Tuple, Optional
import json

ProcessInput7Values = Tuple[float, float, float, int, float, float, float]
ProcessInput6Values = Tuple[float, float, float, int, float, float]
ProcessInput5Values = Tuple[float, float, float, float, float]
InputValues = Tuple[float, float, float]

class GrindingInput(BaseModel):
    work_speed : float
    cut_depth : float
    wheel_speed : float
    
    def from_scalar(other):
        if isinstance(other, GrindingInput):
            return other
        return GrindingInput(work_speed=other, cut_depth=other, wheel_speed=other)
    
    def __add__(self, other):
        other = GrindingInput.from_scalar(other)
        return GrindingInput(work_speed=self.work_speed + other.work_speed,
                             cut_depth=self.cut_depth + other.cut_depth,
                             wheel_speed=self.wheel_speed + other.wheel_speed)
        
    def __sub__(self, other):
        other = GrindingInput.from_scalar(other)
        return GrindingInput(work_speed=self.work_speed - other.work_speed,
                             cut_depth=self.cut_depth - other.cut_depth,
                             wheel_speed=self.wheel_speed - other.wheel_speed)
        
    def __mul__(self, other):
        other = GrindingInput.from_scalar(other)
        return GrindingInput(work_speed=self.work_speed * other.work_speed,
                             cut_depth=self.cut_depth * other.cut_depth,
                             wheel_speed=self.wheel_speed * other.wheel_speed)
        
    def __truediv__(self, other):
        other = GrindingInput.from_scalar(other)
        if other.work_speed == 0.0:
            other.work_speed = 1.0
        if other.cut_depth == 0.0:
            other.cut_depth = 1.0
        if other.wheel_speed == 0.0:
            other.wheel_speed = 1.0
        return GrindingInput(work_speed=self.work_speed / other.work_speed,
                             cut_depth=self.cut_depth / other.cut_depth,
                             wheel_speed=self.wheel_speed / other.wheel_speed)
    
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
    
    @property
    def inputs(self) -> list[GrindingInput]:
        return [self.rough] * self.r_passes + [self.finish]
    
    def __init__(self, **kwargs):
        #print('Creating ProcessInput7:')
        #print(f"rough:{kwargs['rough']}|r_passes:{kwargs['r_passes']}|finish:{kwargs['finish']}")
        super().__init__(inputs=[kwargs['rough']]*int(kwargs['r_passes']) + [kwargs['finish']], **kwargs)
    
    def __str__(self) -> str:
        output = f"Process 7 Inputs:\n"
        output += f"Total cut depth: {self.total_cut_depth}\t No. of passes: {self.n_passes}\n"
        output += f"{self.r_passes}x Rough: {self.rough}\n"
        output += f"Finish  : {self.finish}\n"
        return output
    
    def get_values(self) -> ProcessInput7Values:
        return self.rough.get_values() + [self.r_passes] + self.finish.get_values()
    
    def get_float_values(self) -> list[float]:
        return self.rough.get_values() + self.finish.get_values()

    def from_values(values : ProcessInput7Values):
        return ProcessInput7(rough=GrindingInput.from_values(values[:3]), r_passes=values[3], finish=GrindingInput.from_values(values[4:]))
    
    def from_float_values(values : list[float], r_passes : int):
        return ProcessInput7(rough=GrindingInput.from_values(values[:3]), r_passes=r_passes, finish=GrindingInput.from_values(values[3:]))
    
    def from_g_input(g_input : GrindingInput, r_passes : int):
        return ProcessInput7(rough=g_input, finish=g_input, r_passes=r_passes)
    
    def to_json(self, **kwargs) -> str:
        return f'{{"rough":{self.rough.to_json()}, "r_passes": {self.r_passes}, "finish": {self.finish.to_json()}' + \
            ' '.join([f',"{key}": {kwargs[key]}' for key in kwargs]) + \
    '}'
    
    def from_json(string : str):
        data = json.loads(string)
        return ProcessInput7(**data)
    
    def from_scalar(other):
        if isinstance(other, ProcessInput7):
            return other
        return ProcessInput7(rough=GrindingInput.from_scalar(other), 
                             finish=GrindingInput.from_scalar(other),
                             r_passes=0)
    
    def __add__(self, other):
        other = ProcessInput7.from_scalar(other)
        return ProcessInput7(rough=self.rough + other.rough,
                             finish=self.finish + other.finish,
                             r_passes=self.r_passes + other.r_passes)
        
    def __sub__(self, other):
        other = ProcessInput7.from_scalar(other)
        return ProcessInput7(rough=self.rough - other.rough,
                             finish=self.finish - other.finish,
                             r_passes=self.r_passes - other.r_passes)
        
    def __mul__(self, other):
        other = ProcessInput7.from_scalar(other)
        return ProcessInput7(rough=self.rough * other.rough,
                             finish=self.finish * other.finish,
                             r_passes=self.r_passes * other.r_passes)
        
    def __truediv__(self, other):
        other = ProcessInput7.from_scalar(other)
        if other.r_passes == 0:
            other.r_passes = 1
        return ProcessInput7(rough=self.rough / other.rough,
                             finish=self.finish / other.finish,
                             r_passes=int(self.r_passes / other.r_passes))

    
if __name__ == '__main__':
    print(GrindingInput(work_speed=34, wheel_speed=50, cut_depth=0.03))
    print(ProcessInput(inputs=[GrindingInput(work_speed=34, wheel_speed=50, cut_depth=0.03), GrindingInput(work_speed=34, wheel_speed=50, cut_depth=0.03)],
                       total_cut_depth=3.5))
    print(ProcessInput7(rough=GrindingInput(work_speed=34, wheel_speed=50, cut_depth=0.03), finish=GrindingInput(work_speed=40, wheel_speed=20, cut_depth=0.07), r_passes=4))