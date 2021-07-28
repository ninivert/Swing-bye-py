import pyglet
import numpy as np
from .globals import WINDOW_WIDTH, WINDOW_HEIGHT


class CameraGroup(pyglet.graphics.OrderedGroup):

	def __init__(self, ctx, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ctx = ctx
		self.reset()

	def to_world_space(self, x, y):
		# I still don't understand why this doesn't need scaling...
		return (np.array((x, y)) - self.offset) / self.scale

	def to_screen_space(self, x, y):
		return (np.array((x, y)) / self.scale) + self.offset

	def reset(self):
		self.smooth = True
		self.scale = 0.05
		self.target_scale = 0.5
		self.zoom_anchor = np.zeros(2)
		self.offset = np.array(((WINDOW_WIDTH//2, WINDOW_HEIGHT//2)), dtype=np.float64)
		self.target_offset = np.array(((WINDOW_WIDTH//2, WINDOW_HEIGHT//2)), dtype=np.float64)

	def update(self):
		if self.smooth:
			self.scale = self.lerp(self.scale, self.target_scale, 0.1)
			self.offset = self.lerp(self.offset, self.target_offset, 0.2)
		else:
			self.scale = self.target_scale
			self.offset = self.target_offset

	def lerp(self, value1, value2, percentage):
		return value1 + (value2 - value1) * percentage

	def pan(self, dx, dy):
		self.target_offset += (np.array((dx, dy)))
		self.update()

	def zoom(self, x, y, direction):
		self.zoom_anchor = self.offset + np.array((x, y))
		if direction == 1:
			self.target_scale *= 1.3
		elif direction == -1:
			self.target_scale *= 0.7
		else:
			raise(ValueError(f'direction can only be 1 or -1, but you provided {direction}'))
		self.update()

	def set_state(self):
		pyglet.gl.glPushMatrix()
		pyglet.gl.glTranslatef(*self.offset, 0)
		pyglet.gl.glScalef(self.scale, self.scale, 1)
		pyglet.gl.glTranslatef(*-self.offset, 0)
		pyglet.gl.glTranslatef(*(self.offset), 0)
		self.update()

	def unset_state(self):
		pyglet.gl.glPopMatrix()

