from swingbye.cphysics import Planet as CPlanet
from swingbye.cphysics import vec2

class PyPlanet(CPlanet):
	def __init__(self, *args, **kwargs):
		CPlanet.__init__(self, *args, **kwargs)

	def _get_pos(self):
		print('get pos')
		return super().pos

	def _set_pos(self, pos):
		print('set pos')
		super()._set_pos(pos)

	pos = property(_get_pos, _set_pos)

if __name__ == '__main__':
	p1 = PyPlanet(anchor=vec2(2.0, 3.0))
	p2 = PyPlanet(maxis=5.0)
	p2.set_parent(p1)
	p3 = PyPlanet(maxis=2.0)
	p3.set_parent(p2)

	print('>>> initialized planets')
	print(p1, p2, p3, sep='\n')

	print('>>> positions at time 1')
	print(p1.pos_at(1))
	print(p2.pos_at(1))
	print(p3.pos_at(1))

	print('>>> setting time to 1')
	p1.time = 1
	print(p1.time)
	print(p1.pos)
