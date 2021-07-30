import pyglet
import numpy as np
import json
import logging
from .scene import Scene
from .groups.camera import CameraGroup
from .groups.hud import HUDgroup
from ..components.slider import Base, Knob, Slider
from ..eventmanager import EventManager
from ..utils import create_sprite
from ...physics.ship import Ship
from ...physics.world import World
from ...physics.integrator import EulerIntegrator
from ..gameobjects.planetobject import PlanetObject
from ..gameobjects.shipobject import ShipObject
from ..globals import WINDOW_WIDTH, WINDOW_HEIGHT, DEBUG

_logger = logging.getLogger(__name__)


class Level(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.levels = ['swingbye/levels/level1.json']
		self.level_index = 0
		self.mouse_x = 0
		self.mouse_y = 0

	def on_mouse_motion(self, x, y, dx, dy):
		self.hud.on_mouse_motion(x, y, dx, dy)
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.hud.captured:
			self.hud.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
		else:
			self.camera.pan(dx, dy)
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_press(self, x, y, buttons, modifiers):
		if self.hud.hit(x, y):
			self.hud.on_mouse_press(x, y, buttons, modifiers)

	def on_mouse_release(self, x, y, buttons, modifiers):
		self.hud.on_mouse_release(x, y, buttons, modifiers)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if self.hud.hit(x, y):
			self.hud.on_mouse_scroll(x, y, scroll_x, scroll_y)
		else:
			self.camera.zoom(x, y, scroll_y)

	@staticmethod
	def parse_level(level: dict, batch: pyglet.graphics.Batch, group: pyglet.graphics.OrderedGroup) -> World:
		planets = []
		ship = None
		queue = [(child_dict, None) for child_dict in level['world']]

		while queue:
			child_dict, parent = queue.pop()

			# Convert the position list to a numpy array
			if 'pos' in child_dict:
				child_dict['pos'] = np.array(child_dict['pos'])
			if 'anchor' in child_dict:
				child_dict['anchor'] = np.array(child_dict['anchor'])

			_logger.debug(f'parsing {child_dict}')

			if child_dict['type'] == 'planet':
				planetobject = PlanetObject(
					sprite=create_sprite(child_dict['sprite'], batch=batch, group=group),
					parent=parent,
					**child_dict['arguments']
				)
				queue += [(_child_dict, planetobject) for _child_dict in child_dict['children']]
				planets.append(planetobject)

			elif child_dict['type'] == 'ship':
				if ship is not None:
					_logger.warning(f'more than one ship in level, ignoring')
					_logger.debug(level)
					continue

				ship = ShipObject(
					sprite=create_sprite(child_dict['sprite'], batch=batch, group=group),
					parent=parent,
					**child_dict['arguments']
				)

			else:
				_logger.warning(f'type `{child_dict["type"]}` is not recognized.')

		if ship is None:
			# TODO : world without ship ?
			_logger.warning(f'no ship found, instanciating default ship')
			ship = Ship()

		world = World(ship=ship, planets=planets, integrator=EulerIntegrator)
		_logger.debug(f'finished parsing level, result\n`{world}`')
		return world

	def load(self):
		self.batch = pyglet.graphics.Batch()

		self.paralax = pyglet.graphics.OrderedGroup(0)
		self.camera = CameraGroup(1)
		self.hud = HUDgroup(2)

		self.event_manager.callbacks = {
			'on_mouse_motion': self.on_mouse_motion,
			'on_mouse_drag': self.on_mouse_drag,
			'on_mouse_press': self.on_mouse_press,
			'on_mouse_release': self.on_mouse_release,
			'on_mouse_scroll': self.on_mouse_scroll
		}

		with open(self.levels[self.level_index]) as file:
			level = json.load(file)

		_logger.debug(f'parsing level from file `{self.levels[self.level_index]}`')

		self.world = self.parse_level(level, self.batch, self.camera)

		base = Base(1000, 5, batch=self.batch, group=self.hud)
		knob = Knob(10, batch=self.batch, group=self.hud)
		self.slider = Slider(
			WINDOW_WIDTH//2 - 500, 20,
			base, knob,
			min_value=0, max_value=50000,
			step=25,
			edge=5
		)
		self.hud.add(self.slider)

		if DEBUG:
			self.offset_line = pyglet.shapes.Line(0, 0, 0, 0, color=(255, 20, 20), batch=self.batch, group=self.hud)
			self.mouse_line = pyglet.shapes.Line(0, 0, 0, 0, color=(20, 255, 20), batch=self.batch, group=self.camera)

	def begin(self):
		self.gui.clear()

		self.load()

	def draw(self):
		self.batch.draw()

	def run(self, dt):
		self.hud.update()
		if self.slider.updated:
			self.world.time = self.slider.value

		if DEBUG:
			self.offset_line.x2, self.offset_line.y2 = self.camera.to_screen_space(*self.world.planets[5].pos)
			self.mouse_line.x2, self.mouse_line.y2 = self.camera.to_world_space(self.mouse_x, self.mouse_y)
