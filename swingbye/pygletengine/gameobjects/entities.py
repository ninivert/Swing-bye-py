import math
from random import random
from swingbye.physics.ship import Ship
from swingbye.physics.planet import Planet
from swingbye.physics.entity import ImplicitEntity
from swingbye.physics.collisions import HitZoneDisk
from swingbye.pygletengine.gameobjects.mixins import SpriteMixin, PredictionMixin
from swingbye.pygletengine.globals import GameEntity
from dataclasses import dataclass


@dataclass
class StarObject(SpriteMixin, ImplicitEntity):
	def __post_init__(self):
		scale = 1 + random()
		self.sprite.update(x=self.pos[0], y=self.pos[1], scale=scale)


@dataclass
class ShipObject(SpriteMixin, PredictionMixin, HitZoneDisk, Ship):
	def __post_init__(self):
		self.radius = 10  # set ship hitbox
		scale = self.radius / (self.sprite.width//2)
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

	def delete(self):
		self.sprite.delete()
		self.path.delete()


@dataclass
class PlanetObject(SpriteMixin, PredictionMixin, HitZoneDisk, Planet):
	game_entity: GameEntity = GameEntity.PLANET

	def __post_init__(self):
		scale = self.radius / (self.sprite.height//2)
		self.sprite.update(x=self.pos[0], y=self.pos[1], scale=scale)

	def delete(self):
		self.sprite.delete()
		self.path.delete()

	def __eq__(self, other):
		return self.sprite == other.sprite

	def __hash__(self):
		return hash(self.sprite)

	def __repr__(self):
		return str(self.sprite)
