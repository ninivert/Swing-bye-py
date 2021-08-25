from swingbye.cphysics import Entity, vec2

class PyEntity(Entity):
	def __init__(self):
		Entity.__init__(self)
		self.pointing = False

	def _get_pos(self):
		print('get pos')
		return super().pos

	def _set_pos(self, pos):
		print('set pos')
		super()._set_pos(pos)

	pos = property(_get_pos, _set_pos)

if __name__ == '__main__':
	e = PyEntity()
	print(e.pos)
	e.pos = vec2(3, 4)
	print(e.pos)
	print(e.pointing)
