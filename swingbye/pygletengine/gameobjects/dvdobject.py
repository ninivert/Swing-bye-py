import pyglet
from random import randrange


class DVDobject(pyglet.sprite.Sprite):

	def __init__(self, image_path, x, y, width, height, colors, window_width, window_height, *args, **kwargs):
		image = pyglet.resource.image(image_path)
		super().__init__(image, x=x, y=y, *args, **kwargs)

		self.dx = randrange(100, 250)
		self.dy = randrange(100, 250)
		super().update(scale_x=width/self.width, scale_y=height/self.height)
		self.colors = colors
		self.color_index = 0
		self.color = self.colors[self.color_index]
		
		self.window_width = window_width
		self.window_height = window_height

		noise = pyglet.media.synthesis.WhiteNoise(10)
		self.player = pyglet.media.Player()
		self.player.loop = True
		self.player.volume = 0.005
		self.player.queue(noise)
		self.player.play()

		self.sound = pyglet.resource.media('assets/sounds/bonk.mp3')
		self.sfx = pyglet.media.Player()
		self.sfx.volume = 0.25

	def change_color(self):
		self.color_index = (self.color_index + 1) % len(self.colors)
		self.color = self.colors[self.color_index]

	def borders(self):
		hit_border = False
		if self.x < 0:
			self.x = 0
			self.dx *= -1
			hit_border = True
		elif self.x + self.width > self.window_width:
			self.x = self.window_width - self.width
			self.dx *= -1
			hit_border = True
		if self.y < 0:
			self.y = 0
			self.dy *= -1
			hit_border = True
		elif self.y + self.height > self.window_height:
			self.y = self.window_height - self.height
			self.dy *= -1
			hit_border = True
		if hit_border:
			self.change_color()
			self.sfx.queue(self.sound)
			self.sfx.play()


	def update(self, dt):
		self.x += self.dx * dt
		self.y += self.dy * dt
		self.borders()
