from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
	Pybind11Extension(
		'cphysics',
		['src/pybind.cpp']
	)
]

setup(
	ext_modules=ext_modules
)
