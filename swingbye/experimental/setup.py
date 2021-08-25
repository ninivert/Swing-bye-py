from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
	ext_modules=cythonize(
		Extension(
			'pyvec2d',
			sources=['pyvec2d.pyx'],
			language='c++',
		),
		language_level=3
	)
)

setup(
	ext_modules=cythonize(
		Extension(
			'pyentity',
			sources=['pyentity.pyx'],
			language='c++',
		),
		language_level=3
	)
)
