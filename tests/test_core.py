import cdtriang 
import numpy as np
from timeit import default_timer
import triangle 
from scipy.spatial import Delaunay


def test_core():
    v = np.random.uniform(0,1,(64,2)).astype(np.float32)
    x = cdtriang.triangulate(v)
    return x

def test_speed(niter=10):

    v = np.random.uniform(0,1,(8192,2)).astype(np.float32)

    t1 = default_timer()
    for _ in range(niter):
        x1 = cdtriang.triangulate(v)
    t1 = default_timer()-t1

    t2 = default_timer()
    for _ in range(niter):
        x2 = triangle.triangulate(dict(vertices=v))
    t2 = default_timer()-t2

    t3 = default_timer()
    for _ in range(niter):
        x3 = Delaunay(v)
    t3 = default_timer()-t3

    print(f'cdt:      {t1:.4f}s')
    print(f'triangle: {t2:.4f}s')
    print(f'scipy:    {t3:.4f}s')
    return x1, x2


test_speed()