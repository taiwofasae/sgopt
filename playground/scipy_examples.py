import numpy as np
from functools import partial
from scipy.optimize import minimize

def rosen(x, a, b):
    """ The Rosenbrock function"""
    return sum(a*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0) + b

partial_rosen = partial(rosen, a=0.5, b=1.)

x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])

res = minimize(rosen, x0, method='nelder-mead', args=(0.5, 1.),
               options={'xatol': 1e-8, 'disp': True})

print(res.x)