from libcpp.vector cimport vector, vector
from libcpp cimport bool
cimport cython
import numpy as np
cimport numpy as np


cdef extern from "core.hpp":
    void _triangulate(float * vertices, const int n_vertices,
                      vector[vector[int]] triangles)
    void _triangulate_constrained(float * vertices, const int n_vertices,
                                  int * edges, const int n_edges,
                                  vector[vector[int]] triangles,
                                  const int mode)

    
def triangulate(vertices):
    """
    Delaunay triangulation of a set of 2d vertices

    Parameters
    ----------
    vertices: ndarray, float
          the coordinates of the vertices (N,2)

    Returns
    -------
    triangles: ndarray, int
          the triangles (N,3)          
    """
    if not vertices.ndim==2 and vertices.shape[1]==2:
        raise ValueError(f'vertices should have shape (N,2)')
    
    cdef np.ndarray[float, ndim=2] _vertices
    _vertices = np.ascontiguousarray(vertices, dtype=np.float32)
    cdef vector[vector[int]] _triangles
    _triangulate(&_vertices[0,0], len(_vertices), _triangles)
    return np.asarray(_triangles)


def triangulate_constrained(vertices, edges, remove_outer=False):
    """
    Constrained delaunay triangulation of a set of 2d vertices 
    and given edges (i.e. a delaunay triangulation containing edges)

    Parameters
    ----------
    vertices: ndarray, float
          the coordinates of the vertices (N,2)
    edges: ndarray, int
          the edges that need to be aprt of the triangulation (N,2)

    Returns
    -------
    triangles: ndarray, int
          the triangles (N,3)          
    """
    if not vertices.ndim==2 and vertices.shape[1]==2:
        raise ValueError(f'vertices should have shape (N,2)')
    if not edges.ndim==2 and edges.shape[1]==2:
        raise ValueError(f'edges should have shape (N,2)')

    cdef np.ndarray[float, ndim=2] _vertices,
    cdef np.ndarray[int, ndim=2] _edges
    _vertices = np.ascontiguousarray(vertices, dtype=np.float32)
    _edges    = np.ascontiguousarray(edges, dtype=np.int32)
    cdef vector[vector[int]] _triangles
    _triangulate_constrained(&_vertices[0,0], len(_vertices),
                             &_edges[0,0], len(_edges),
                             _triangles, remove_outer)
    return np.asarray(_triangles)



