cdef extern from "vec2.h":
	cdef cppclass vec2d:
		double x
		double y

		vec2d()
		vec2d(double, double)
		vec2d(vec2d&)

		vec2d& operator=(vec2d&)

		vec2d operator+(vec2d&)
		vec2d operator-(vec2d&)

		# vec2d& operator+=(vec2d&)
		# vec2d& operator-=(vec2d&)

		vec2d operator+(double)
		vec2d operator-(double)
		vec2d operator*(double)
		vec2d operator/(double)

		# vec2d& operator+=(double)
		# vec2d& operator-=(double)
		# vec2d& operator*=(double)
		# vec2d& operator/=(double)

		void set(double, double)

		void rotate(double)

		vec2d& normalize()

		double length()
		void truncate(double)

		vec2d ortho()

		@staticmethod
		double dist(vec2d, vec2d)
		@staticmethod
		double dot(vec2d, vec2d)
		@staticmethod
		double cross(vec2d, vec2d)
