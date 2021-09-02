import logging
from swingbye.cphysics import Entity as CEntity
from swingbye.cphysics import vec2
from swingbye.logic.mixins import PredictionMixin
from swingbye.globals import SHIP_PREDICTION_N, SHIP_LAUNCH_SPEED

_logger = logging.getLogger(__name__)

class Ship(CEntity, PredictionMixin):
	def __init__(self, *args, **kwargs):
		CEntity.__init__(self, *args, **kwargs)
		PredictionMixin.__init__(self, SHIP_PREDICTION_N)

		self.parent = None
		self.time = 0.0

		self._pointing = vec2(0.0, 1.0)
		self.pointing = vec2(0.0, 1.0)

	@property
	def docked(self):
		return self.parent is not None

	# Time updating (keeping track of the docked ship on the planet)

	def _get_time(self):
		return self._time

	def _set_time(self, time: float):
		self._time = time
		if self.docked:
			self.update_docked_pos()

	time = property(_get_time, _set_time)

	# Pointing

	def _get_pointing(self):
		if self.docked:
			return self._pointing
		else:
			# When initializing, pointing is called to generate the field, however at the parent may not be yet initialized
			speed = self.vel.length()
			if speed == 0.0:
				ret = vec2(0.0, 1.0)
				_logger.warning(f'divide by zero encountered in `_get_pointing`, returning `{ret}`')
				return ret
			return self.vel / speed

	def _set_pointing_safe(self, pointing):
		if not self.docked:
			_logger.warning('cannot point ship that is launched, ignoring')
			return

		self._set_pointing(pointing)

		if self.docked:
			self.update_docked_pos()

	def _set_pointing(self, pointing):
		self._pointing = pointing

	pointing = property(_get_pointing, _set_pointing_safe)

	# Game logic

	def launch(self):
		_logger.info('launching ship')

		if not self.docked:
			_logger.warning('cannot launch a ship that is not docked, ignoring')
			return

		# Set the ship velocity
		v0 = self.pointing*(SHIP_LAUNCH_SPEED + self.parent.vel.length())
		self.vel = v0

		# Undock the ship
		self.parent = None

	def update_docked_pos(self):
		if self.docked:
			self.pos = self.parent.pos_at(self.time) + self.pointing*(self.parent.radius + 10)
		else:
			_logger.warning('trying to update docked position, but the ship is launched, ignoring')
