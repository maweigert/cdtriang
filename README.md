# cdtriang (Demo)

Experimental python bindings via cython for https://github.com/artem-ogre/CDT

### Install 

```
git clone git@github.com:maweigert/cdtriang.git
pip install -e cdtriang
```


### Usage

```python

from cdtriang.core import triangulate, triangulate_constrained

vertices = np.array([[0, 0],[0,1],[1,1],[1,0]])

tri = triangulate(vertices)

print(tri)


>>> [[1 2 0]
     [2 3 0]]

```


