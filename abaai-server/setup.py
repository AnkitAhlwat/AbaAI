from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize("abalone/ai/cython/cython_clumping_agent.pyx")
)