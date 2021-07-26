import pyglet
from .globals import WINDOW_WIDTH, WINDOW_HEIGHT


class DVD(pyglet.shapes.Rectangle):

	def __init__(self, x, y, width, height, colors, *args, **kwargs):
		super().__init__(x, y, width, height, *args, **kwargs)

		self.dx = 90
		self.dy = 123
		self.colors = colors
		self.color_index = 0
		self.color = self.colors[self.color_index]

	def change_color(self):
		self.color_index = (self.color_index + 1) % len(self.colors)
		self.color = self.colors[self.color_index]

	def borders(self):
		if self.x < 0:
			self.x = 0
			self.dx *= -1
			self.change_color()
		elif self.x + self.width > WINDOW_WIDTH:
			self.x = WINDOW_WIDTH - self.width
			self.dx *= -1
			self.change_color()
		if self.y < 0:
			self.y = 0
			self.dy *= -1
			self.change_color()
		elif self.y + self.height > WINDOW_HEIGHT:
			self.y = WINDOW_HEIGHT - self.height
			self.dy *= -1
			self.change_color()

	def update(self, dt):
		self.x += self.dx * dt
		self.y += self.dy * dt
		self.borders()


class Level:

	def __init__(self, ctx):
		self.ctx = ctx
		self.current_level = 0
		self.total_levels = 10

	def begin(self):
		
		self.ctx.gui.clear()

		self.dvd = DVD(0, 0, 100, 40, [
			(255, 20, 20),
			(20, 255, 20),
			(20, 20, 255),
			(255, 255, 20),
			(255, 20, 255)],
			batch=self.ctx.batch
		)

		self.ctx.game_loop = self.run

	def run(self, dt):
		self.dvd.update(dt)
