import math
import random

def Get_random_vector(dim):
    res = []
    res_norm = 0
    for i in range(dim):
        coordinate = (random.random() - 0.5) * 2
        res_norm += coordinate**2
        res.append(coordinate)
    for i in range(dim):
        res[i] /= math.sqrt(res_norm)
    return res

def Scalar_vectors(x,y):
    return sum(x[i]*y[i] for i in range(len(x)))

def Cos(x, y):
    return Scalar_vectors(x,y) / (math.sqrt(Scalar_vectors(x,x)) * math.sqrt(Scalar_vectors(y,y)) + 1e-10)