import pyglet
import numpy as np


class ParallaxGroup(pyglet.graphics.OrderedGroup):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.parallax_factor = 10
		self._world_offset = np.zeros(2)
		self._parallax_offset = np.zeros(2)

	@property
	def world_offset(self):
		return self._world_offset

	@world_offset.setter
	def world_offset(self, world_offset):
		self._parallax_offset = world_offset / self.parallax_factor
		self._world_offset = world_offset

	def set_state(self):
		pyglet.gl.glPushMatrix()
		pyglet.gl.glTranslatef(*self._parallax_offset, 0)

	def unset_state(self):
		pyglet.gl.glPopMatrix()