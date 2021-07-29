import numpy as np
import logging
from dataclasses import dataclass, field
from typing import Union
from .entity import ImplicitEntity
from ..globals import SHIP_LAUNCH_SPEED

_logger = logging.getLogger(__name__)

@dataclass
class Ship(ImplicitEntity):
	# Parent
	# NOTE : type hint is `'Planet'` instead of `Planet`,
	# since the class is not defined at this point
	parent: Union[None, 'Ship'] = None
	time: float
	_time: float = field(init=False, repr=False, default=0.0)
	pointing: np.ndarray
	_pointing: np.ndarray = field(init=False, repr=False, default=np.array([0.0, 1.0]))

	# Time updating (keeping track of the docked ship on the planet)

	@property
	def time(self):
		return self._time

	@time.setter
	def time(self, time: float):
		if type(time) is property:
			time = Ship._time
		self._time = time

		if self.docked:
			self.pos = self.parent.pos_at(time) + self.pointing*self.parent.radius

	# Docked

	@property
	def docked(self):
		return self.parent is not None

	# Pointing

	@property
	def pointing(self):
		if self.docked:
			return self._pointing
		else:
			return self.vel / np.linalg.norm(self.vel)

	@pointing.setter
	def pointing(self, pointing):
		if type(pointing) is property:
			pointing = Ship._pointing

		if not self.docked:
			_logger.warning('cannot point ship that is launched, ignoring')
			return

		self._pointing = pointing

	# Game logic

	def launch(self):
		if not self.docked:
			_logger.warning('cannot launch a ship that is not docked, ignoring')
			return

		# Set the ship velocity
		v0 = self.pointing*(SHIP_LAUNCH_SPEED + np.linalg.norm(self.parent.vel))
		self.vel = v0

		# Undock the ship
		self.parent = None
