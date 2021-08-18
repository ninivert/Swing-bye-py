import pyglet
from ...utils import clamp, lerp
from ...globals import WINDOW_WIDTH, WINDOW_HEIGHT


class Camera:
	""" A simple 2D camera that contains the speed and offset."""

	def __init__(self, window, min_zoom=0.2, max_zoom=4, parent=None):
		assert min_zoom <= max_zoom, "Minimum zoom must not be greater than maximum zoom"

		self.smooth = True

		self.window = window

		self.offset_x = 0
		self.offset_y = 0
		self.target_offset_x = self.offset_x
		self.target_offset_y = self.offset_y
		self.parent_offset_x = 0
		self.parent_offset_y = 0
		self.anchor_x = self.window.width//2
		self.anchor_y = self.window.width//2

		self.set_zoom_limits(min_zoom, max_zoom)
		self.zoom = max(min(2, self.max_zoom), self.min_zoom)
		self.target_zoom = self.zoom

		self.set_parent(parent)

	def world_to_screen(self, x, y):
		return ((x - self.offset_x) * self.zoom + self.anchor_x, (y - self.offset_y) * self.zoom + self.anchor_y)

	def screen_to_world(self, x, y):
		return (self.offset_x + (x - self.anchor_x) / self.zoom, self.offset_y + (y - self.anchor_y) / self.zoom)

	def set_zoom_limits(self, min_zoom, max_zoom):
		self.min_zoom = min_zoom
		self.max_zoom = max_zoom

	def set_parent(self, parent):
		self.parent = parent
		if self.parent is None:
			self.target_offset_x += self.parent_offset_x
			self.target_offset_y += self.parent_offset_y
			self.parent_offset_x, self.parent_offset_y = 0, 0
		else:
			self.parent_offset_x, self.parent_offset_y = self.world_to_screen(*self.parent.pos)

	def move(self, dx, dy):
		self.target_offset_x += dx / self.zoom
		self.target_offset_y += dy / self.zoom

	def zoom_at(self, x, y, direction):
		self.offset_x += (x - self.anchor_x) / self.zoom
		self.offset_y += (y - self.anchor_y) / self.zoom
		self.target_offset_x += (x - self.anchor_x) / self.zoom
		self.target_offset_y += (y - self.anchor_y) / self.zoom
		self.anchor_x = x
		self.anchor_y = y
		if direction == 1:
			self.target_zoom *= 1.3
		elif direction == -1:
			self.target_zoom *= 0.7
		else:
			raise ValueError(f'direction must be -1 or 1, but you provided {direction}')
		self.target_zoom = clamp(self.target_zoom, self.min_zoom, self.max_zoom)

	def update(self):
		if self.parent is not None:
			self.parent_offset_x, self.parent_offset_y = self.parent.pos
		if self.smooth:
			self.zoom = lerp(self.zoom, self.target_zoom, 0.2)
			self.offset_x = lerp(self.offset_x, self.target_offset_x + self.parent_offset_x, 0.2)
			self.offset_y = lerp(self.offset_y, self.target_offset_y + self.parent_offset_y, 0.2)
		else:
			self.zoom = self.target_zoom
			self.offset_x = self.target_offset_x + self.parent_offset_x
			self.offset_y = self.target_offset_y + self.parent_offset_y

	def begin(self):
		self.update()
		x = -self.anchor_x/self.zoom + self.offset_x
		y = -self.anchor_y/self.zoom + self.offset_y

		pyglet.gl.glTranslatef(-x * self.zoom, -y * self.zoom, 0)

		pyglet.gl.glScalef(self.zoom, self.zoom, 1)

	def end(self):
		x = -self.anchor_x/self.zoom + self.offset_x
		y = -self.anchor_y/self.zoom + self.offset_y

		pyglet.gl.glScalef(1 / self.zoom, 1 / self.zoom, 1)

		pyglet.gl.glTranslatef(x * self.zoom, y * self.zoom, 0)

	def __enter__(self):
		self.begin()

	def __exit__(self, exception_type, exception_value, traceback):
		self.end()
