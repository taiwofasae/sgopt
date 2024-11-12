import math
from scipy.optimize import minimize

C1 = 0.15
C2 = 50
C3 = 50
C4 = 25
C5 = 300
C6 = 3.142


def dP1(R, dRdt, K, phi):
    return (C6*C6/8.) * \
        (C1*((R*R+R*C2)/K)*(dRdt)-2*C4*C4) * \
            (math.log((R*(C4+C2)/(C4*(R+C2))))) / \
                C2

def dP2(R, dRdt, h, dhdt, K, phi):
    return phi - h - C2 + (C2/K)*(dhdt)


def obj_fun(R, dRdt, h, dhdt, K, phi):
    return math.abs(dP1(R, dRdt, K, phi) - dP2(R, dRdt, h, dhdt, K, phi))

def generate_obj_fun(R, dRdt, h, dhdt):
    return lambda x: obj_fun(R, dRdt, h, dhdt, x[0], x[1])

R, dRdt, h, dhdt = 52.021481, 0, 290, 0
res = minimize(generate_obj_fun(R, dRdt, h, dhdt),
               method='trust-constr',
               options={'verbose': 1})

print(res.x)
K, phi = res.x[0], res.x[1]
print(f'K={K}')
print(f'phi={phi}')
print(f'dP1={dP1(R, dRdt, K, phi)}')
print(f'dP2={dP2(R, dRdt, h, dhdt, K, phi)}')


