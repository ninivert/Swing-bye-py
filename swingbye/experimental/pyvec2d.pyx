# distutils: language = c++

from vec2 cimport vec2d

# Inspired from
# https://stackoverflow.com/questions/33764094/cython-how-do-i-wrap-a-c-class-where-public-member-variables-are-custom-objec

cdef class PyVec2d:
	cdef vec2d* cptr_vec2d
	cdef object owner  # None if this is our own

	def __cinit__(self, double x=0, double y=0):
		self.cptr_vec2d = new vec2d(x, y)

	cdef set_ptr(self, vec2d* ptr, owner):
		if self.owner is None:
			del self.cptr_vec2d
		self.cptr_vec2d = ptr
		self.owner = owner

	def __dealloc__(self):
		# only free if we own it
		if self.owner is None:
			del self.cptr_vec2d

	property x:
		def __get__(self):
			return self.cptr_vec2d[0].x
		def __set__(self, double x):
			self.cptr_vec2d[0].x = x

	property y:
		def __get__(self):
			return self.cptr_vec2d[0].y
		def __set__(self, double y):
			self.cptr_vec2d[0].y = y

	# TODO : wrap the rest of c++ functions of vec2.h ?
