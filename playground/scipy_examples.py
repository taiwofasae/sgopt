import numpy as np
from functools import partial
from scipy.optimize import minimize, Bounds, LinearConstraint, NonlinearConstraint


bounds = Bounds([0, -0.5], [1.0, 2.0]) # lb, ub
linear_constraint = LinearConstraint([[1, 2], [2, 1]], [-np.inf, 1], [1, 1]) 
# matrix (N x d), lb, ub

def rosen(x):
    """ The Rosenbrock function"""
    return sum((x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])

res = minimize(rosen, x0, method='nelder-mead',
               options={'xatol': 1e-8, 'disp': True})

print(res.x)

# Nonlinear constraint

def cons_f(x):
    return [x[0]**2 + x[1], x[0]**2 - x[1]]
def cons_J(x):
    return [[2*x[0], 1], [2*x[0], -1]]
def cons_H(x, v):
    return v[0]*np.array([[2, 0], [0, 0]]) + v[1]*np.array([[2, 0], [0, 0]])
nonlinear_constraint = NonlinearConstraint(cons_f, -np.inf, 1, jac=cons_J, hess=cons_H) 
# fun: vector -> N function evals (Nx1), lb=-np.inf, ub=1

x0 = np.array([0.5, 0])
res = minimize(rosen, x0, method='trust-constr',
               constraints=[linear_constraint, nonlinear_constraint],
               options={'verbose': 1}, bounds=bounds)

print(res.x)