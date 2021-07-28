import pyglet
import numpy as np
import json
import logging
from .globals import WINDOW_WIDTH, WINDOW_HEIGHT
from .camera import CameraGroup
from .hud import HUDgroup, wtfisthis
from .utils import create_sprite
from ..physics.ship import Ship
from ..physics.world import World
from ..physics.integrator import EulerIntegrator
from ..gameobjects.planetobject import PlanetObject
from ..gameobjects.shipobject import ShipObject

_logger = logging.getLogger(__name__)

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
		self.levels = ['swingbye/views/levels/level1.json']
		self.level_index = 0

	def parse_level(self, level: dict) -> World:
		planets = []
		ship = None
		queue = [(child_dict, None) for child_dict in level['world']]

		while queue:
			child_dict, parent = queue.pop()

			# Convert the position list to a numpy array
			if 'x' in child_dict:
				child_dict['x'] = np.array(child_dict['x'])

			_logger.debug(f'parsing {child_dict}')

			if child_dict['type'] == 'planet':
				planetobject = PlanetObject(
					create_sprite(child_dict['sprite'], batch=self.ctx.batch, group=self.camera),
					**dict(parent=parent, **child_dict['arguments'])
				)
				queue += [(_child_dict, planetobject) for _child_dict in child_dict['children']]
				planets.append(planetobject)

			elif child_dict['type'] == 'ship':
				if ship is not None:
					_logger.warning(f'more than one ship in level, ignoring')
					_logger.debug(level)
					continue

				ship = ShipObject(
					create_sprite(child_dict['sprite'], batch=self.ctx.batch, group=self.camera),
					**dict(parent=parent, **child_dict['arguments'])
				)

			else:
				_logger.warning(f'type `{child_dict["type"]}` is not recognized.')

		if ship is None:
			# TODO : world without ship ?
			_logger.warning(f'no ship found, instanciating default ship')
			ship = Ship()

		world = World(ship, planets, EulerIntegrator())
		_logger.debug(f'finished parsing level, result\n`{world}`')
		return world

	def load_level(self):
		self.paralax = pyglet.graphics.OrderedGroup(0)
		self.camera = CameraGroup(self.ctx, 1)
		self.hud = HUDgroup(2)

		with open(self.levels[self.level_index]) as file:
			level = json.load(file)

		_logger.debug(f'parsing level from file `{self.levels[self.level_index]}`')

		self.world = self.parse_level(level)
		self.line = pyglet.shapes.Line(0, 0, 0, 0, color=(255, 20, 20), batch=self.ctx.batch, group=self.hud)
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
