if __name__ == '__main__':
	from swingbye.cphysics import Planet, vec2

	p1 = Planet(anchor=vec2(2.0, 3.0))
	p2 = Planet(maxis=5.0)
	p2.set_parent(p1)
	p3 = Planet(maxis=2.0)
	p3.set_parent(p2)

	print('>>> initialized planets')
	print(p1, p2, p3, sep='\n')

	print('>>> positions at time 0')
	print(p1.pos_at(0))
	print(p2.pos_at(0))
	print(p3.pos_at(0))

	print('>>> positions at time 1')
	print(p1.pos_at(1))
	print(p2.pos_at(1))
	print(p3.pos_at(1))

	print('>>> timing 1000 position computation at random times')
	from time import time
	from random import uniform
	start = time()
	for _ in range(1000):
		p3.pos_at(uniform(0, 100))
	end = time()
	print(f'{end-start:.6f}s')
