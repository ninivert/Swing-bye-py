if __name__ == '__main__':
	import math
	from swingbye.cphysics import vec2

	print('>>> initializers')
	print(vec2())
	print(vec2(3, 4))

	print('>>> to_tuple()')
	print(vec2(3, 4).to_tuple())

	print('>>> operators with vec2')
	print(vec2(3, 4) + vec2(4, 5))
	print(vec2(3, 4) - vec2(4, 5))
	v1 = vec2(3, 4)
	v1 += vec2(4, 5)
	print(v1)
	v2 = vec2(3, 4)
	v2 -= vec2(4, 5)
	print(v2)

	print('>>> operators with floats')
	print(10 + vec2(4, 5))
	print(10 - vec2(4, 5))
	print(10 * vec2(4, 5))
	print(10 / vec2(4, 5))
	print(vec2(4, 5) + 10)
	print(vec2(4, 5) - 10)
	print(vec2(4, 5) * 10)
	print(vec2(4, 5) / 10)

	print('>>> rotate()')
	e1 = vec2(1, 0)
	e1.rotate(math.pi/2)
	print(e1)

	print('>>> normalize()')
	v3 = vec2(3, 4)
	v3.normalize()
	print(v3)

	print('>>> length()')
	print(vec2(3, 4).length())

	print('>>> ortho()')
	print(vec2(1, 0).ortho())

	print('>>> vec2.dist()')
	print(vec2.dist(vec2(0, 0), vec2(3, 4)))

	print('>>> vec2.dot()')
	print(vec2.dot(vec2(1, 0), vec2(2, 5)))

	print('>>> vec2.cross()')
	print(vec2.cross(vec2(1, 0), vec2(2, 5)))
