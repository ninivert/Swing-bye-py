raise NotImplementedError('This code is deprecated and is thus commented out')

# import pyglet
# import numpy as np


# class ParallaxGroup(pyglet.graphics.OrderedGroup):
# 	def __init__(self, order, rate=1, parent=None):
# 		super().__init__(order=order, parent=parent)
# 		self.rate = rate
# 		self.offset = np.zeros(2)
# 		self.scale_x = 1
# 		self.scale_y = 1

# 	def update(self, scale_x=1, scale_y=1):
# 		self.scale_x = scale_x
# 		self.scale_y = scale_y

# 	def set_state(self):
# 		pyglet.gl.glTranslatef(*-(self.offset*self.rate), 0)
# 		pyglet.gl.glScalef(self.scale_x, self.scale_y, 1)

# 	def unset_state(self):
# 		pyglet.gl.glScalef(1/self.scale_x, 1/self.scale_y, 1)
# 		pyglet.gl.glTranslated(*(self.offset*self.rate), 0)
