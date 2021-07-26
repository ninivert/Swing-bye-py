import numpy as np
from .entity import ImplicitEntity

class Ship(ImplicitEntity):
	def __init__(
		self,
		x: np.ndarray = np.zeros(2),  # position
		v: np.ndarray = np.zeros(2),  # velocity
		m: np.ndarray = 1,   # mass
		parent=None  # parent planet if docked
	):
		self.parent = parent
		self.predicted = []  # TODO : predicted path
		super().__init__(x, v, m)

	@property
	def docked(self):
		return self.parent is not None

	def __str__(self):
		ret = super().__str__()
		ret += f'\n\tpos {self.x}, vel {self.v}, ass {self.m}, parent {self.parent}'
		return ret
