import abc
import numpy as np

class Entity():
	def __init__(
		self,
		x: np.ndarray = np.zeros(2),  # position
		m: np.ndarray = 1   # mass
	):
		self.x = x
		self.m = m

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
		m: np.ndarray = 1   # mass
	):
		self.v = v
		super().__init__(x, m)
