import pyglet
import numpy as np
from ...utils import clamp
from ...globals import WINDOW_WIDTH, WINDOW_HEIGHT


class CameraGroup(pyglet.graphics.OrderedGroup):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.smooth = True
		self.set_scale_limits(0.2, 4)
		self.min_offset = None
		self.max_offset = None

		self.reset()

	def to_world_space(self, x: float, y: float) -> np.ndarray:
		return (np.array((x, y)) - (self.offset + self.default_offset)) / self.scale

	def to_screen_space(self, x: float, y: float) -> np.ndarray:
		return (np.array((x, y)) * self.scale) + (self.offset + self.default_offset)

	def set_bounding_box(self, min_world, max_world):
		self.min_offset = self.to_screen_space(*min_world)
		self.max_offset = self.to_screen_space(*max_world)

	def set_scale_limits(self, min_scale, max_scale):
		self.min_scale = min_scale
		self.max_scale = max_scale

	def reset(self):
		self.scale = 1
		self.target_scale = 1
		self.zoom_anchor = np.zeros(2)
		self.default_offset = np.array((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), dtype=np.float64)
		self.offset = np.zeros(2)
		self.target_offset = np.zeros(2)

	def update(self):
		self.target_scale = clamp(self.target_scale, self.min_scale, self.max_scale)
		if self.min_offset and self.max_offset:
			self.target_offset[0] = clamp(self.target_offset[0], self.min_offset[0], self.max_offset[0])
			self.target_offset[1] = clamp(self.target_offset[1], self.min_offset[1], self.max_offset[1])
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
		pyglet.gl.glTranslatef(*(self.offset + self.default_offset), 0)
		pyglet.gl.glScalef(self.scale, self.scale, 1)
		# pyglet.gl.glTranslatef(*-(self.offset + self.default_offset), 0)
		# pyglet.gl.glTranslatef(*(self.offset + self.default_offset), 0)
		self.update()

	def unset_state(self):
		pyglet.gl.glPopMatrix()

