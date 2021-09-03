import math
from random import random
from swingbye.cphysics import Entity
from swingbye.logic.ship import Ship
from swingbye.logic.planet import Planet
from swingbye.logic.collisions import HitZoneDisk
from swingbye.pygletengine.gameobjects.mixins import SpriteMixin, PathMixin
from swingbye.pygletengine.globals import GameEntity
from swingbye.pygletengine.components.paths import LinePath
from swingbye.globals import PLANET_PREDICTION_N, SHIP_PREDICTION_N

class StarObject(SpriteMixin, Entity):
	def __init__(self, *args, **kwargs):
		if 'sprite' in kwargs:
			SpriteMixin.__init__(self, sprite=kwargs['sprite'])
			del kwargs['sprite']

		Entity.__init__(self, *args, **kwargs)

		scale = 1 + random()
		self.sprite.update(x=self.pos.x, y=self.pos.y, scale=scale)

	def delete(self):
		self.sprite.delete()


class ShipObject(SpriteMixin, PathMixin, HitZoneDisk, Ship):
	def __init__(self, *args, **kwargs):
		if 'sprite' in kwargs:
			SpriteMixin.__init__(self, sprite=kwargs['sprite'])
			del kwargs['sprite']
		else:
			SpriteMixin.__init__(self)

		if 'path' in kwargs:
			PathMixin.__init__(self, path=kwargs['path'])
			del kwargs['path']
		else:
			PathMixin.__init__(self, path=LinePath(point_count=SHIP_PREDICTION_N))

		if 'radius' in kwargs:
			HitZoneDisk.__init__(self, radius=kwargs['radius'])
			del kwargs['radius']
		else:
			HitZoneDisk.__init__(self)

		Ship.__init__(self, *args, **kwargs)

		self.radius = 10  # set ship hitbox
		scale = self.radius / (self.sprite.width//2)
		self.sprite.update(x=self.pos.x, y=self.pos.y, scale=scale)

	# TODO : move pointing logic to a mixin

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
		self.sprite.rotation = -math.degrees(math.atan2(pointing.y, pointing.x)) + 90

	pointing = property(_get_pointing, Ship._set_pointing_safe)

	def delete(self):
		self.sprite.delete()
		self.path.delete()


class PlanetObject(SpriteMixin, PathMixin, HitZoneDisk, Planet):
	def __init__(self, *args, **kwargs):
		# TODO : clean this up !

		if 'sprite' in kwargs:
			SpriteMixin.__init__(self, sprite=kwargs['sprite'])
			del kwargs['sprite']
		else:
			SpriteMixin.__init__(self)

		if 'path' in kwargs:
			PathMixin.__init__(self, path=kwargs['path'])
			del kwargs['path']
		else:
			# TODO : Planet already has a prediction mixin,
			# read from the prediction mixin to init the LinePath
			PathMixin.__init__(self, path=LinePath(point_count=PLANET_PREDICTION_N))

		if 'radius' in kwargs:
			HitZoneDisk.__init__(self, radius=kwargs['radius'])
			del kwargs['radius']
		else:
			HitZoneDisk.__init__(self)

		if 'game_entity' in kwargs:
			self.game_entity = GameEntity.PLANET
			del kwargs['game_entity']

		if 'name' in kwargs:
			self.name = kwargs['name']
			del kwargs['name']
		else:
			self.name = 'planet'

		Planet.__init__(self, *args, **kwargs)

		scale = self.radius / (self.sprite.height//2)
		self.sprite.update(x=self.pos.x, y=self.pos.y, scale=scale)
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
