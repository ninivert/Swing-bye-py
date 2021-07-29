from abc import abstractmethod, ABCMeta
from dataclasses import dataclass, field
import numpy as np
import math


@dataclass
class ImplicitEntity:
	"""A simulated mass-point. pos and vel should be solved using physics.integrator"""
	mass: float = 1.0
	pos: np.ndarray = np.zeros(2)
	vel: np.ndarray = np.zeros(2)


@dataclass
class ExplicitEntity(metaclass=ABCMeta):
	"""An entity where the equations of movement have explicit solutions at any time"""
	# Note : ExplicitEntity doesn't share a class `Entity` with ImplicitEntity,
	# since here pos and vel are read-only
	mass: float = 1.0
	time: float
	_time: float = field(init=False, repr=False, default=0.0)
	_pos: np.ndarray = field(init=False, repr=False, default=np.zeros(2))
	_vel: np.ndarray = field(init=False, repr=False, default=np.zeros(2))
	_dirty_pos: bool = field(init=True, repr=False, default=False)
	_dirty_vel: bool = field(init=True, repr=False, default=False)

	@abstractmethod
	def pos_at(self, time: float) -> np.ndarray:
		pass

	@abstractmethod
	def vel_at(self, time: float) -> np.ndarray:
		pass

	@property
	def pos(self):
		if self._dirty_pos:
			self._pos = self.pos_at(self.time)
			self._dirty_pos = False
		return self._pos

	@property
	def vel(self):
		if self._dirty_vel:
			self._vel = self.vel_at(self.time)
			self._dirty_vel = False
		return self._vel

	@property
	def time(self):
		return self._time

	@time.setter
	def time(self, value: float):
		if type(value) is property:
			value = ExplicitEntity._time
		self._time = value
		self._dirty_pos = True
		self._dirty_vel = True


if __name__ == '__main__':
	@dataclass
	class CircularExplicitEntity(ExplicitEntity):
		def pos_at(self, time: float) -> np.ndarray:
			print(f'>>> computing position of `{self}`')
			return np.array([math.cos(time), math.sin(time)])

		def vel_at(self, time: float) -> np.ndarray:
			print(f'>>> computing velocity of `{self}`')
			return np.array([-math.sin(time), math.cos(time)])

	e3 = ImplicitEntity()
	e3.exert_force(np.array([0.0, -1.0]))
	print(e3, sep='\n')

	try:
		e3 = ExplicitEntity()
	except TypeError as error:
		print(f'>>> correctly caught following error : {error}')

	e4 = CircularExplicitEntity()
	e4.time = 2
	e4.pos
	e4.pos
	e4.time = 3
	e4_pos2 = e4.pos
	e4_pos1 = CircularExplicitEntity.pos_at(e4, 3)
	print(e4)
	assert((e4_pos1 == e4_pos2).all())
	print('>>> passed position test for `CircularExplicitEntity`')
