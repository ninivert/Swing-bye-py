# distutils: sources = entity.cpp

from vec2 cimport vec2d

cdef extern from "entity.h" namespace "entity":
	cdef cppclass Entity:
		vec2d pos
		vec2d vel
		double mass

		Entity()
		Entity(vec2d, vec2d, double)
