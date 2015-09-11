import sys
import random

def Get_random_vector(dim):
    res = []
    res_norm = 0
    for i in range(dim):
        coordinate = random.random()
        res_norm += coordinate**2
        res.append(coordinate)
    for i in range(dim):
        res[i] /= res_norm
    return res

def Scalar_vectors(x,y):
    return sum(x[i]*y[i] for i in range(len(x)))