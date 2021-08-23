from ...physics.ship import Ship
from .utils import SpriteMixin, PredictionMixin
from dataclasses import dataclass
import math

@dataclass
class ShipObject(SpriteMixin, PredictionMixin, Ship):
	def __post_init__(self):
		scale = 0.05  # self.r / (self.sprite.width//2)
		self.sprite.update(x=self.pos[0], y=self.pos[1], scale=scale)

	def _get_vel(self):
		return super().vel

	def _set_vel(self, pos):
		super()._set_vel(pos)
		# HACK : we override _set_vel, because it gets called while the game is running,
		# so that we can orient the ship in the correct direction
		self._set_pointing(self._get_pointing())

	vel = property(_get_vel, _set_vel)

	def _get_pointing(self):
		return super().pointing

	def _set_pointing(self, pointing):
		super()._set_pointing(pointing)
		if type(pointing) is not property:
			self.sprite.rotation = -math.degrees(math.atan2(pointing[1], pointing[0])) + 90

	pointing = property(_get_pointing, Ship._set_pointing_safe)
