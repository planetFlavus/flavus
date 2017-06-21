from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="generator",
    ext_modules = cythonize("generator.pyx")
        
)
