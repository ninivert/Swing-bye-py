import numpy as np
import logging
from .entity import ImplicitEntity
from ..globals import SHIP_PREDICTION_N, SHIP_LAUNCH_SPEED

_logger = logging.getLogger(__name__)

class Ship(ImplicitEntity):
	def __init__(
		self,
		x: np.ndarray = np.zeros(2),  # position
		v: np.ndarray = np.zeros(2),  # velocity
		m: np.ndarray = 1,   # mass
		parent=None  # parent planet if docked
	):
		self.parent = parent
		self.predicted = np.zeros((SHIP_PREDICTION_N, 2))  # TODO : predicted path
		self._pointing = np.array([1., 0.])
		super().__init__(x, v, m)

	@property
	def docked(self):
		return self.parent is not None

	@property
	def pointing(self):
		if self.docked:
			return self._pointing
		else:
			return self.v / np.linalg.norm(self.v)

	@pointing.setter
	def pointing(self, pointing):
		if self.docked:
			self._pointing = pointing
		else:
			_logger.warning('cannot point ship that is launched, ignoring')

	def launch(self):
		# Set the ship velocity
		v0 = self.pointing*(SHIP_LAUNCH_SPEED + np.linalg.norm(self.parent.get_vel(self.t)))
		self.v = v0

		# Undock the ship
		self.parent = None

	def __str__(self):
		ret = super().__str__()
		ret += f'\n\tpos {self.x}, vel {self.v}, ass {self.m}, parent {self.parent}'
		return ret
