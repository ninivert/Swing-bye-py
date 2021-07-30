import pyglet
import glooey
import numpy as np
import json
import logging
from .scene import Scene
from .groups.camera import CameraGroup
from .groups.hud import HUDgroup
from ..components.slider import Base, Knob, Slider
from ..eventmanager import EventManager
from ..utils import create_sprite, clamp, point_in_rect
from ...physics.ship import Ship
from ...physics.world import World, WorldStates
from ...physics.integrator import EulerIntegrator
from ..gameobjects.planetobject import PlanetObject
from ..gameobjects.shipobject import ShipObject
from ..globals import WINDOW_WIDTH, WINDOW_HEIGHT, DEBUG

_logger = logging.getLogger(__name__)


###############
# HUD Classes #
###############


class HUDContainer(glooey.HBox):
	custom_cell_padding = 5
	custom_alignment = 'fill'


class HUDButtonLabel(glooey.Label):
	custom_alignment = 'center'
	custom_font_size = 26


class HUDButton(glooey.Button):
	Foreground = HUDButtonLabel
	custom_alignment = 'fill'

	def __init__(self, *args, action=None, action_params=[], **kwargs):
		super().__init__(*args, **kwargs)
		self.action = action
		self.action_params = action_params

	def on_click(self, widget):
		if self.action:
			self.action(*self.action_params)

	class Base(glooey.Background):
		custom_color = '#aa1e1e'

	class Over(glooey.Background):
		custom_color = '#cc3f3f'

	class Down(glooey.Background):
		custom_color = '#ff5d5d'


class HUDSlider(Slider):
	custom_alignment = 'fill'


#############


class Level(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.levels = ['swingbye/levels/level1.json']
		self.level_index = 0
		self.mouse_x = 0
		self.mouse_y = 0

	def on_mouse_motion(self, x, y, dx, dy):
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if point_in_rect(x, y, *self.hud_rect.bottom_left, *self.hud_rect.size) or self.slider.captured:
			self.slider.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
		else:
			self.camera.pan(dx, dy)
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_release(self, x, y, dx, dy):
		self.slider.on_mouse_release(x, y, dx, dy)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if not point_in_rect(x, y, *self.hud_rect.bottom_left, *self.hud_rect.size):
			self.camera.zoom(x, y, scroll_y)

	def on_resize(self, width, height):
		self.hud_rect = self.hud_container.get_rect()  # haha get rekt

	def on_slider_value_update(self, value):
		if self.world.state == WorldStates.PRE_LAUNCH:
			self.world.time = value

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

	def load_hud(self):
		self.container = glooey.VBox()
		self.hud_container = HUDContainer()

		reset = HUDButton('Reset')
		pause = HUDButton('Pause')
		self.slider = HUDSlider(
			self.on_slider_value_update,
			min_value=0, max_value=50000,
			step=25,
			edge=10
		)
		launch = HUDButton('LAUNCH', action=self.launch_ship)

		self.hud_container.pack(reset)
		self.hud_container.pack(pause)
		self.hud_container.add(self.slider)
		self.hud_container.pack(launch)

		self.container.add(glooey.Bin())
		self.container.add(self.hud_container, size=0)

		self.gui.add(self.container)

		self.hud_rect = self.hud_container.get_rect()

	def load(self):
		self.batch = pyglet.graphics.Batch()

		self.paralax = pyglet.graphics.OrderedGroup(0)
		self.camera = CameraGroup(1)
		# This is no longer needed since we are now using glooey for the hud
		self.hud = HUDgroup(2)
		# Waiting to delete

		self.event_manager.callbacks = {
			'on_mouse_motion': self.on_mouse_motion,
			'on_mouse_drag': self.on_mouse_drag,
			'on_mouse_release': self.on_mouse_release,
			'on_mouse_scroll': self.on_mouse_scroll,
			'on_resize': self.on_resize
		}

		with open(self.levels[self.level_index]) as file:
			level = json.load(file)

		_logger.debug(f'parsing level from file `{self.levels[self.level_index]}`')

		self.world = self.parse_level(level, self.batch, self.camera)

		if DEBUG:
			self.offset_line = pyglet.shapes.Line(0, 0, 0, 0, color=(255, 20, 20), batch=self.batch, group=self.hud)
			self.mouse_line = pyglet.shapes.Line(0, 0, 0, 0, color=(20, 255, 20), batch=self.batch, group=self.camera)

	def begin(self):
		self.gui.clear()
		self.load()
		self.load_hud()

	def draw(self):
		self.batch.draw()
		self.gui.batch.draw()

	def run(self, dt):
		if self.world.state == WorldStates.POST_LAUNCH:
			self.world.step(dt*100)

		if DEBUG:
			self.offset_line.x2, self.offset_line.y2 = self.camera.to_screen_space(*self.world.planets[0].pos)
			self.mouse_line.x2, self.mouse_line.y2 = self.camera.to_world_space(self.mouse_x, self.mouse_y)

	# Game logic

	def launch_ship(self):
		self.world.launch_ship()
