import abc
import numpy as np

# TODO: this needs to be rewritten
# explicitentity needs to have class methods which set the entity time, compute stuff, then set is back

class Entity():
	def __init__(
		self,
		x: np.ndarray = np.zeros(2),  # position
		m: float = 1   # mass
	):
		self._x = x
		self._m = m

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, x):
		self._x = x

	@property
	def m(self):
		return self._m

	@m.setter
	def m(self, m):
		self._m = m


class ExplicitEntity(Entity, abc.ABC):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@abc.abstractmethod
	def get_vel(self, t: float) -> np.ndarray:
		raise NotImplementedError()

	@abc.abstractmethod
	def get_pos(self, t: float) -> np.ndarray:
		raise NotImplementedError()

class ImplicitEntity(Entity, abc.ABC):
	def __init__(
		self,
		x: np.ndarray = np.zeros(2),  # position
		v: np.ndarray = np.zeros(2),  # velocity
		m: float = 1   # mass
	):
		self._v = v
		super().__init__(x, m)

	@property
	def v(self):
		return self._v

	@v.setter
	def v(self, v):
		self._v = v
