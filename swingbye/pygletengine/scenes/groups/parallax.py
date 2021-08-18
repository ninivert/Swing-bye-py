import pyglet
import numpy as np


class ParallaxGroup(pyglet.graphics.OrderedGroup):
	def __init__(self, order, rate=1, parent=None):
		super().__init__(order=order, parent=parent)
		self.rate = rate
		self._cam_pos = np.zeros(2)

	def move_camera(self, dx, dy):
		self._cam_pos += (dx * self.rate, dy * self.rate)

	def set_state(self):
		pyglet.gl.glTranslatef(*self._cam_pos, 0)

	def unset_state(self):
		pyglet.gl.glTranslated(*-self._cam_pos, 0)
