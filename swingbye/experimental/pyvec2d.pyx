# distutils: language = c++

from vec2 cimport vec2d

cdef class PyVec2d:
	cdef vec2d* c_vec2d_ptr

	def __cinit__(self, double x=0, double y=0):
		self.c_vec2d_ptr = new vec2d(x, y)

	def __dealloc__(self):
		del self.c_vec2d_ptr

	property x:
		def __get__(self):
			return self.c_vec2d_ptr[0].x
		def __set__(self, double x):
			self.c_vec2d_ptr[0].x = x

	property y:
		def __get__(self):
			return self.c_vec2d_ptr[0].y
		def __set__(self, double y):
			self.c_vec2d_ptr[0].y = y

	# @staticmethod
	# cdef PyVec2d create_view(vec2d other):
	# 	ret_pyvec2d = PyVec2d()
	# 	ret_pyvec2d.c_vec2d_ptr = &other
	# 	return ret_pyvec2d

	# TODO : wrap the rest of c++ functions of vec2.h ?
