import numpy as np
import logging
from dataclasses import dataclass, field
from typing import Union
from .entity import ImplicitEntity
from ..globals import SHIP_LAUNCH_SPEED, SHIP_PREDICTION_N

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
	prediction: np.ndarray
	_prediction: np.ndarray = field(init=False, repr=False, default=np.zeros((SHIP_PREDICTION_N, 2)))

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
			self.update_docked_pos()

	# Docked

	@property
	def docked(self):
		return self.parent is not None

	# Pointing

	def _get_pointing(self):
		if self.docked:
			return self._pointing
		else:
			# When initializing, pointing is called to generate the field, however at the parent may not be yet initialized
			speed = np.linalg.norm(self.vel)
			if speed == 0.0:
				_logger.warning('divide by zero encountered in `_get_pointing`, returning default `Ship._pointing`')
				return Ship._pointing
			return self.vel / speed

	def _set_pointing_safe(self, pointing):
		if not self.docked:
			_logger.warning('cannot point ship that is launched, ignoring')
			return

		self._set_pointing(pointing)

		if self.docked:
			self.update_docked_pos()

	def _set_pointing(self, pointing):
		if type(pointing) is property:
			pointing = Ship._pointing

		self._pointing = pointing

	pointing = property(_get_pointing, _set_pointing_safe)

	# Prediction

	def _get_prediction(self):
		return self._prediction

	def _set_prediction(self, prediction):
		if type(prediction) is property:
			prediction = Ship._prediction

		self._prediction = prediction

	prediction = property(_get_prediction, _set_prediction)

	# Game logic

	def launch(self):
		_logger.info('launching ship')

		if not self.docked:
			_logger.warning('cannot launch a ship that is not docked, ignoring')
			return

		# Set the ship velocity
		v0 = self.pointing*(SHIP_LAUNCH_SPEED + np.linalg.norm(self.parent.vel))
		self.vel = v0

		# Undock the ship
		self.parent = None

	def update_docked_pos(self):
		if self.docked:
			self.pos = self.parent.pos_at(self.time) + self.pointing*self.parent.radius
		else:
			_logger.warning('trying to update docked position, but the ship is launched, ignoring')
