import pyglet
import numpy as np


class ParallaxGroup(pyglet.graphics.OrderedGroup):
	def __init__(self, order, rate=1, parent=None):
		super().__init__(order=order, parent=parent)
		self.rate = rate
		self.offset = np.zeros(2)

	def set_state(self):
		pyglet.gl.glTranslatef(*-(self.offset*self.rate), 0)

	def unset_state(self):
		pyglet.gl.glTranslated(*(self.offset*self.rate), 0)
