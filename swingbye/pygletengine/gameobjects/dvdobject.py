import pyglet


class DVDobject(pyglet.shapes.Rectangle):

	def __init__(self, x, y, width, height, colors, window_width, window_height *args, **kwargs):
		super().__init__(x, y, width, height, *args, **kwargs)

		self.dx = 90
		self.dy = 123
		self.colors = colors
		self.color_index = 0
		self.color = self.colors[self.color_index]
		self.window_width = window_width
		self.window_height = window_height

	def change_color(self):
		self.color_index = (self.color_index + 1) % len(self.colors)
		self.color = self.colors[self.color_index]

	def borders(self):
		if self.x < 0:
			self.x = 0
			self.dx *= -1
			self.change_color()
		elif self.x + self.width > self.window_width:
			self.x = self.window_width - self.width
			self.dx *= -1
			self.change_color()
		if self.y < 0:
			self.y = 0
			self.dy *= -1
			self.change_color()
		elif self.y + self.height > self.window_height:
			self.y = self.window_height - self.height
			self.dy *= -1
			self.change_color()

	def update(self, dt):
		self.x += self.dx * dt
		self.y += self.dy * dt
		self.borders()
