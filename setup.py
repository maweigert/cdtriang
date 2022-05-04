from setuptools import setup, Extension
import numpy as np
from Cython.Distutils import build_ext

extension = Extension('cdtriang.core',
                      ['cdtriang/core.pyx'],
                      include_dirs=[np.get_include(), 'cdtriang/_vendored'],
                      language="c++",
                      extra_compile_args = ["-O3", "-std=c++11"],
                      )



setup(
    name='cdtriang',
    version='0.0.1',
    description='Demo wrapper around CDT',
    author='Martin Weigert',
    author_email='marweigert@gmail.com',
    url='https://github.com/maweigert/cdtriang',    
    packages=['cdtriang'],
    ext_modules=[extension],
    cmdclass={"build_ext": build_ext},
)
