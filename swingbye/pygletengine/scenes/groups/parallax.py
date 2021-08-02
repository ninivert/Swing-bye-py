import pyglet
import numpy as np


class ParallaxGroup(pyglet.graphics.OrderedGroup):

	def __init__(self, parallax_factor, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.parallax_factor = parallax_factor
		self.scale_x = 1
		self.scale_y = 1
		self._offset = np.zeros(2)
		self._parallax_offset = np.zeros(2)

	@property
	def offset(self):
		return self._offset

	@offset.setter
	def offset(self, offset):
		self._parallax_offset = offset / self.parallax_factor
		self._offset = offset

	def set_state(self):
		pyglet.gl.glPushMatrix()
		pyglet.gl.glScalef(self.scale_x, self.scale_y, 0)
		pyglet.gl.glTranslatef(*self._parallax_offset, 0)

	def unset_state(self):
		pyglet.gl.glPopMatrix()
