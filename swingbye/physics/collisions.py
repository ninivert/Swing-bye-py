import abc
import numpy as np

class HitZone(metaclass=abc.ABCMeta):
	def collides_with(self, other: 'HitZone'):
		return collides(self, other)

class HitZonePoint(HitZone):
	def __init__(self, pos=np.zeros(2)):
		self.pos = pos

class HitZoneDisk(HitZone):
	def __init__(self, radius=1, pos=np.zeros(2)):
		self.radius = radius
		self.pos = pos


class HitZoneRect(HitZone):
	def __init__(self, pos=np.zeros(2), dims=np.ones(2)):
		self.pos = pos
		self.dims = dims


def collides(obj1: HitZone, obj2: HitZone, firstcall=True) -> bool:
	if type(obj1) is HitZoneDisk and type(obj2) is HitZoneDisk:
		return np.linalg.norm(obj1.pos - obj2.pos) <= obj1.radius + obj2.radius

	if type(obj1) is HitZoneRect and type(obj2) is HitZonePoint:
		return (obj1.pos[0] <= obj2.pos[0] <= obj1.pos[0] + obj1.dims[0]) and (obj1.pos[1] <= obj2.pos[1] <= obj1.pos[1] + obj1.dims[1])

	# Collision is commutative, so we need to check both "directions"
	if firstcall:
		return collides(obj2, obj1, False)

	raise NotImplementedError(f'collision between {type(obj1)} and {type(obj2)} is not implemented')


if __name__ == '__main__':
	print(f'>>> testing collisions between {HitZoneDisk} and {HitZoneDisk}')

	d1 = HitZoneDisk(pos=np.array([0, 0]))
	d2 = HitZoneDisk(pos=np.array([0, 0.5]))
	d3 = HitZoneDisk(pos=np.array([0, 2]))
	d4 = HitZoneDisk(pos=np.array([0, 2.1]))

	assert(collides(d1, d2))
	assert(collides(d2, d1))
	assert(collides(d2, d3))
	assert(collides(d3, d2))
	assert(collides(d1, d3))
	assert(collides(d3, d1))
	assert(not collides(d1, d4))
	assert(not collides(d4, d1))

	print('OK')

	print(f'>>> testing collisions between {HitZoneRect} and {HitZonePoint}')

	r1 = HitZoneRect(pos=np.array([0, 0]), dims=np.array([200, 100]))
	p1 = HitZonePoint(pos=np.array([0, 0]))
	p2 = HitZonePoint(pos=np.array([100, 50]))
	p3 = HitZonePoint(pos=np.array([200, 200]))
	p4 = HitZonePoint(pos=np.array([300, 200]))

	assert(collides(r1, p1))
	assert(collides(p1, r1) == collides(r1, p1))  # testing associativity
	assert(collides(r1, p2))
	assert(not collides(r1, p3))
	assert(not collides(r1, p4))

	print('OK')
