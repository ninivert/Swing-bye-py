import pyglet
import numpy as np
from swingbye.pygletengine.utils import clamp, lerp


class Camera:

	def __init__(self, window, min_zoom=0.2, max_zoom=4, smooth=True, smooth_level=0.05, parent=None):
		assert min_zoom <= max_zoom, "Minimum zoom must not be greater than maximum zoom"

		# Flag(s)
		self.smooth = smooth
		self.smooth_level = smooth_level

		# For getting the window size, that's it...
		self.window = window

		# For camera movement
		self.offset = np.zeros(2)
		self.target_offset = self.offset
		self.parent_offset = np.zeros(2)
		self.anchor = np.array((self.window.width//2, self.window.height//2))

		# Zooming and scaling
		self.set_zoom_limits(min_zoom, max_zoom)
		self.zoom = max(min(1, self.max_zoom), self.min_zoom)
		self.target_zoom = self.zoom

		# Assign parent
		self.set_parent(parent)

	def on_resize(self, width, height):
		self.anchor = np.array((width//2, height//2))

	def world_to_screen(self, x, y):
		return (np.array((x, y)) - self.offset) * self.zoom + self.anchor

	def screen_to_world(self, x, y):
		return self.offset + (np.array((x, y)) - self.anchor) / self.zoom

	def set_zoom_limits(self, min_zoom, max_zoom):
		self.min_zoom = min_zoom
		self.max_zoom = max_zoom

	def set_parent(self, parent):
		self.parent = parent
		if self.parent is not None:
			self.target_offset *= 0
			self.anchor = np.array((self.window.width//2, self.window.height//2))
			self.parent_offset = self.parent.pos.copy()

	def set_position(self, x, y):
		self.offset = np.array((-x, -y))
		self.target_offset = np.array((-x, -y))

	def set_anchor(self, x, y):
		self.anchor = np.array((x, y))

	def set_zoom(self, zoom):
		self.zoom = zoom
		self.target_zoom = zoom

	def move(self, dx, dy):
		self.target_offset += (dx / self.zoom, dy / self.zoom)

	def zoom_at(self, x, y, direction):
		# When camera is tracking something, zoom around it and not the cursor
		if self.parent is not None:
			x, y = self.world_to_screen(*self.parent.pos)

		# Correct the offset to zoom at the correct place (black magic, do not touch)
		self.offset += (np.array((x, y)) - self.anchor) / self.zoom
		self.target_offset += (np.array((x, y)) - self.anchor) / self.zoom
		self.anchor = np.array((x, y))

		# Do the zooming
		# could use np.exp for constant zoom levels (but "breaks" with lerp)
		if direction == 1:
			self.target_zoom *= 1.3
		elif direction == -1:
			self.target_zoom *= 0.7
		else:
			raise ValueError(f'direction must be -1 or 1, but you provided {direction}')

		# Don't zoom too far tho
		self.target_zoom = clamp(self.target_zoom, self.min_zoom, self.max_zoom)

	def update(self):
		if self.parent is not None:
			# Copy to avoid destroying the object's position
			self.parent_offset = self.parent.pos.copy()
		if self.smooth:
			smooth = lambda a, b, t: a + (b-a)*(1 - pow(1 - t, 3))
			self.zoom = smooth(self.zoom, self.target_zoom, self.smooth_level)
			self.offset = smooth(self.offset, self.target_offset + self.parent_offset, self.smooth_level)
		else:
			self.zoom = self.target_zoom
			self.offset = self.target_offset + self.parent_offset

	def begin(self):
		self.update()
		x, y = -self.anchor / self.zoom + self.offset

		pyglet.gl.glEnable(pyglet.gl.GL_BLEND)

		pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

		pyglet.gl.glTranslatef(-x * self.zoom, -y * self.zoom, 0)

		pyglet.gl.glScalef(self.zoom, self.zoom, 1)

	def end(self):
		x, y = -self.anchor / self.zoom + self.offset

		pyglet.gl.glDisable(pyglet.gl.GL_BLEND)

		pyglet.gl.glScalef(1 / self.zoom, 1 / self.zoom, 1)

		pyglet.gl.glTranslatef(x * self.zoom, y * self.zoom, 0)

	def __enter__(self):
		self.begin()

	def __exit__(self, exception_type, exception_value, traceback):
		self.end()
