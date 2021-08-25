# distutils: language = c++

# https://stackoverflow.com/questions/33764094/cython-how-do-i-wrap-a-c-class-where-public-member-variables-are-custom-objec

from entity cimport Entity
from vec2 cimport vec2d
from .pyvec2d import PyVec2d

cdef class PyEntity:
	cdef Entity* cptr_entity

	def __cinit__(self, pos: PyVec2d=PyVec2d(), vel: PyVec2d=PyVec2d(), double mass=1.0):
		# Does not work apparently, I think it doesn't know c_vec2d is in fact a vec2d
		# self.c_entity = Entity(pos.c_vec2d, vel.c_vec2d, mass)

		self.cptr_entity = new Entity(vec2d(pos.x, pos.y), vec2d(vel.x, vel.y), mass)

	property pos:
		def __get__(self):
			pos = PyVec2d()
			cptr_entity = self.cptr_entity
			pos.set_ptr(&(cptr_entity.pos), self)
			return pos
