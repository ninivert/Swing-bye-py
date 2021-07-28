import pyglet
import numpy as np
from .globals import WINDOW_WIDTH, WINDOW_HEIGHT
from .camera import CameraTransformGroup
from ..physics.ship import Ship
from ..physics.world import World
from ..physics.integrator import EulerIntegrator
from ..gameobjects.planet import PlanetObject


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

class AxisCross:

	class Axis(pyglet.shapes.Line):
		axis_dict = {
			'x': (0, 0, 50, 0),
			'y': (0, 0, 0, 50)
		}

		def __init__(self, axis, *args, **kwargs):
			super().__init__(*self.axis_dict[axis], *args, **kwargs)

	def __init__(self, batch, group):
		self.x = self.Axis('x', batch=batch, group=group, color=(255, 20, 20))
		self.y = self.Axis('y', batch=batch, group=group, color=(20, 255, 20))



class Level:

	def __init__(self, ctx):
		self.ctx = ctx
		self.current_level = 0
		self.total_levels = 10

	def load_level(self):

		self.paralax = pyglet.graphics.OrderedGroup(0)
		self.camera = CameraTransformGroup(self.ctx, 1)
		self.ui = pyglet.graphics.OrderedGroup(2)

		ship = Ship()

		planet1_img = pyglet.resource.image('assets/sprites/planet1.png')
		planet2_img = pyglet.resource.image('assets/sprites/planet2.png')
		planet3_img = pyglet.resource.image('assets/sprites/planet3.png')
		planet4_img = pyglet.resource.image('assets/sprites/planet4.png')
		planet6_img = pyglet.resource.image('assets/sprites/planet5.png')
		planet5_img = pyglet.resource.image('assets/sprites/star1.png')
		planet1_img.anchor_x = planet1_img.width//2
		planet1_img.anchor_y = planet1_img.height//2
		planet2_img.anchor_x = planet2_img.width//2
		planet2_img.anchor_y = planet2_img.height//2
		planet3_img.anchor_x = planet3_img.width//2
		planet3_img.anchor_y = planet3_img.height//2
		planet4_img.anchor_x = planet4_img.width//2
		planet4_img.anchor_y = planet4_img.height//2
		planet5_img.anchor_x = planet5_img.width//2
		planet5_img.anchor_y = planet5_img.height//2
		planet6_img.anchor_x = planet6_img.width//2
		planet6_img.anchor_y = planet6_img.height//2


		planet1 = pyglet.sprite.Sprite(planet1_img, batch=self.ctx.batch, group=self.camera)
		planet2 = pyglet.sprite.Sprite(planet2_img, batch=self.ctx.batch, group=self.camera)
		planet3 = pyglet.sprite.Sprite(planet3_img, batch=self.ctx.batch, group=self.camera)
		planet4 = pyglet.sprite.Sprite(planet4_img, batch=self.ctx.batch, group=self.camera)
		planet5 = pyglet.sprite.Sprite(planet5_img, batch=self.ctx.batch, group=self.camera)
		planet6 = pyglet.sprite.Sprite(planet6_img, batch=self.ctx.batch, group=self.camera)

		sun = PlanetObject(planet5, r=200, x=np.array([0, 0]), m=20)
		planets = [
			sun,
			earth := PlanetObject(planet1, r=20, s=400, parent=sun),
			moon := PlanetObject(planet6, r=5, s=34, parent=earth),
			PlanetObject(planet2, r=2, s=8, parent=moon),
			PlanetObject(planet3, r=55, s=600, parent=sun),
			PlanetObject(planet4, r=32, s=800, parent=sun),
		]

		ìntegrator = EulerIntegrator()
		self.world = World(ship, planets, ìntegrator)

		self.line = pyglet.shapes.Line(0, 0, 0, 0, color=(255, 20, 20), batch=self.ctx.batch, group=self.ui)
		self.mouse_line = pyglet.shapes.Line(0, 0, 0, 0, color=(20, 255, 20), batch=self.ctx.batch, group=self.camera)

	def begin(self):
		
		self.ctx.gui.clear()

		self.load_level()

		# self.dvd = DVD(0, 0, 100, 40, [
		# 	(255, 20, 20),
		# 	(20, 255, 20),
		# 	(20, 20, 255),
		# 	(255, 255, 20),
		# 	(255, 20, 255)],
		# 	batch=self.ctx.batch
		# )

		self.ctx.game_loop = self.run

	def run(self, dt):
		# self.dvd.update(dt)
		self.world.t += dt * 1000
		self.line.x2, self.line.y2 = self.camera.to_screen_space(*self.world.planets[0].x)
		self.mouse_line.x2, self.mouse_line.y2 = self.camera.to_world_space(self.ctx.mouse_x, self.ctx.mouse_y)