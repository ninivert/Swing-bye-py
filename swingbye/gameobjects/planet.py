import pyglet
import numpy
from ..physics.planet import Planet


class PlanetObject(Planet):

	def __init__(self, sprite, radius, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.sprite = sprite
		scale = radius/(self.sprite.width//2)
		self.sprite.update(x=self.x[0], y=self.x[1], scale=scale)

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, x):
		self.sprite.position = x[0], x[1]
		self._x = x