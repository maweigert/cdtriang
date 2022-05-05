import triangle
import pytest
import cdtriang.core as core
from timeit import default_timer
import numpy as np

def sort2d(x):
    x = np.sort(x, axis=1)
    x = x[np.lexsort(np.rot90(x))]
    return x


def single_triang(n=6, plot=True, _assert=False, niter=10, constrained=False, seed=None, verbose=False):

    if seed is None:
        # beware seed=88 is a fixed point
        # np.random.seed(88);np.random.randint(100)==88
        seed = np.random.randint(2**16)
        
    np.random.seed(seed)
    
    if constrained:
        v = np.random.uniform(-1,1,(n,2)).astype(np.float32)
        v += .4*np.random.uniform(-1,1,(n,2)).astype(np.float32)

        
        edges = np.empty((n,2), np.int32)
        edges[:,0] = np.arange(n)
        edges[:,1] = edges[:,0]+1
        edges[-1,1] = 0
            
    else:
        v = np.random.uniform(-1,1,(n,2)).astype(np.float32)
        edges = None

    v = v.round(4)
    
    t1 = default_timer()
    if edges is not None:
        tri1 = core.triangulate_constrained(v, edges, remove_outer=False)
    else:
        tri1 = core.triangulate(v)
    t1 = default_timer() - t1
    
    t2 = default_timer()
    if edges is not None:    
        tri2 = triangle.triangulate(dict(vertices=v, segments=edges))['triangles']
    else:
        tri2 = triangle.triangulate(dict(vertices=v))['triangles']
        
    t2 = default_timer() - t2

    if verbose:
        print('vertices')
        print(', '.join(f'{{{_v[1]:.4f}, {_v[0]:.4f}}}'for _v in v))
        print('edges')
        print(', '.join(f'{{{_e[0]}, {_e[1]}}}'for _e in edges))


        print('cdtriang')
        print(tri1)
        print('triangle')
        print(tri2)
    
    if plot:
        import matplotlib.pyplot as plt
        plt.ion()
        plt.clf()
        plt.plot(*v.T[::-1], '.', color='C0')

        for i,_v in enumerate(v):
            plt.text(*_v[::-1]+0.01, i)

        if len(tri1)>0:
            plt.triplot(*v.T[::-1], tri1, color='C1', lw=3, label ='cdtriang')

        plt.triplot(*v.T[::-1], tri2, color='C2', lw=1, label='triangle')
        
        if edges is not None:
            for e in edges:
                plt.plot(*v[e].T[::-1], "k-", lw=3, alpha=.2)

        plt.legend()
        plt.axis('equal')

    if tri1.shape == tri2.shape:
        _close = np.allclose(sort2d(tri1),sort2d(tri2))
    else:
        _close = False

        
    print(f'{n=},{seed=},{constrained=}   {1000*t1:.5f} ms   vs   {1000*t2:.5f} ms  -> {_close}')

    if _assert:
        assert _close

    return v, edges
    

@pytest.mark.parametrize("n", (3,4,5,6,7,8,9,11,101,1001,10001))
@pytest.mark.parametrize("constrained", (False, True))
@pytest.mark.parametrize("seed", range(2))
def test_triangulate(n, constrained, seed):
    single_triang(n, plot=False, constrained=constrained, _assert=True, seed=seed)



def test_many():
    for c in (True, False, ):
        for n in (3,4,5,6,7,8,9,11,101,1001,10001):
            for seed in range(1000 if n<11 else 10):
                single_triang(n, plot=False, constrained=c, _assert=False, seed=seed)


if __name__ == '__main__':


    v, edges = single_triang(n=4,seed=0,constrained=True, verbose=True)

