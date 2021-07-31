import pyglet
import glooey
import numpy as np
import json
import logging
from random import randrange
from .scene import Scene
from .groups.parallax import ParallaxGroup
from .groups.camera import CameraGroup
from ..components.slider import Slider
from ..components.graph import Graph
from ..components.buttons import Button, CycleButton
from ..components.containers import VBox, HBox, Board
from ..utils import create_sprite, clamp, point_in_rect
from ...physics.ship import Ship
from ...physics.world import World, WorldStates
from ...physics.integrator import EulerIntegrator, RK4Integrator
from ..gameobjects.planetobject import PlanetObject
from ..gameobjects.shipobject import ShipObject
from ..gameobjects.starobject import StarObject
from ..gameobjects.backgroundobject import BackgroundObject
from ..globals import WINDOW_WIDTH, WINDOW_HEIGHT, DEBUG

_logger = logging.getLogger(__name__)


class Level(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.levels = ['swingbye/levels/level1.json']
		self.level_index = 0

		# TODO : cleanup this
		self.mouse_press_x = 0
		self.mouse_press_y = 0

		self.simulation_speed = 1
		self.paused = False

		self.mouse_x = 0
		self.mouse_y = 0

	def on_mouse_motion(self, x, y, dx, dy):
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.time_slider.captured:
			self.time_slider.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
		elif self.speed_slider.captured:
			self.speed_slider.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
		else:
			self.camera.pan(dx, dy)
			for layer in self.parallax_layers:
				layer.world_offset = self.camera.offset
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_press(self, x, y, buttons, modifiers):
		self.mouse_press_x = x
		self.mouse_press_y = y

	def on_mouse_release(self, x, y, dx, dy):
		clicked = self.mouse_press_x == x and self.mouse_press_y == y

		if not point_in_rect(x, y, *self.hud_rect.bottom_left, *self.hud_rect.size):
			if clicked:
				self.world.point_ship(self.camera.to_world_space(x, y))

		self.time_slider.on_mouse_release(x, y, dx, dy)
		self.speed_slider.on_mouse_release(x, y, dx, dy)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if not point_in_rect(x, y, *self.hud_rect.bottom_left, *self.hud_rect.size):
			self.camera.zoom(x, y, scroll_y)

	def on_resize(self, width, height):
		self.hud_rect = self.hud_container.get_rect()  # haha get rekt
		self.background.update(
			scale_x=width/self.background.width,
			scale_y=height/self.background.height
		)

	def on_time_slider_value_update(self, value):
		if self.world.state == WorldStates.PRE_LAUNCH:
			self.world.time = value

	def on_speed_slider_value_update(self, value):
		self.simulation_speed = int(value)

	def on_pause_button_pressed(self, state):
		if state == 'PAUSED':
			self.paused = True
		elif state == 'NOT PAUSED':
			self.paused = False

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
					# name=child_dict['name'],
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

		world = World(ship=ship, planets=planets, integrator=RK4Integrator)
		_logger.debug(f'finished parsing level, result\n`{world}`')
		return world

	def load_hud(self):
		self.container = glooey.VBox()
		self.hud_container = glooey.HBox()
		board = Board()

		self.graph = Graph(
			100, 100,
			y_scale_mode='fixed_min',
			min_y=0,
			query=lambda: np.linalg.norm(self.world.ship.vel)
		)
		self.graph.hide()
		board.add(self.graph, left=10, bottom=10)

		reset = Button('Reset', action=self.reset)
		pause = CycleButton({'NOT PAUSED': 'Pause', 'PAUSED': 'Resume'}, state_change_callback=self.on_pause_button_pressed)
		self.speed_slider = Slider(
			self.on_speed_slider_value_update,
			min_value=1, max_value=16,
			step=1,
			edge=10
		)
		self.time_slider = Slider(
			self.on_time_slider_value_update,
			min_value=0, max_value=50000,
			step=25,
			edge=10
		)
		launch = Button('LAUNCH', action=self.launch_ship)

		self.hud_container.pack(reset)
		self.hud_container.pack(pause)
		self.hud_container.add(self.speed_slider, size=100)
		self.hud_container.add(self.time_slider)
		self.hud_container.pack(launch)

		self.container.add(board)
		self.container.add(self.hud_container, size=0)

		self.gui.add(self.container)

		self.hud_rect = self.hud_container.get_rect()

	def load_level(self):
		with open(self.levels[self.level_index]) as file:
			level = json.load(file)

		self.background = create_sprite(level['background_sprite'], anchor='bottom_left', size=(WINDOW_WIDTH, WINDOW_HEIGHT), batch=self.batch, group=self.background_layer)
		self.background.opacity = 180

		_logger.debug(f'parsing level from file `{self.levels[self.level_index]}`')

		self.world = self.parse_level(level, self.batch, self.camera)
	
	def load_background(self):
		self.stars = []
		stars_img = [
			'assets/sprites/particle_star1_1.png',
			'assets/sprites/particle_star1_2.png',
			'assets/sprites/particle_star2_1.png',
			'assets/sprites/particle_star2_2.png'
		]
		for i in range(100):
			self.stars.append(
				StarObject(
					pos=np.random.rand(2)*np.array((WINDOW_WIDTH, WINDOW_HEIGHT)),
					sprite=create_sprite(
						np.random.choice(stars_img),
						size=(5, 5),
						batch=self.batch,
						group=np.random.choice(self.parallax_layers)
					)
				)
			)

	def load(self):
		self.batch = pyglet.graphics.Batch()

		self.parallax_layers = [
			ParallaxGroup(35, 0),
			ParallaxGroup(25, 1),
			ParallaxGroup(20, 2)
		]
		self.background_layer = pyglet.graphics.OrderedGroup(3)
		self.camera = CameraGroup(4)
		self.top_layer = pyglet.graphics.OrderedGroup(5)

		# self.add_event_handlers(
		# 	self.on_mouse_motion,
		# 	self.on_mouse_drag,
		# 	self.on_mouse_press,
		# 	self.on_mouse_release,
		# 	self.on_mouse_scroll,
		# 	self.on_resize
		# )

		if DEBUG:
			self.offset_line = pyglet.shapes.Line(0, 0, 0, 0, color=(255, 20, 20), batch=self.batch, group=self.top_layer)
			self.mouse_line = pyglet.shapes.Line(0, 0, 0, 0, color=(20, 255, 20), batch=self.batch, group=self.camera)

		self.load_level()
		self.load_hud()
		self.load_background()

	def begin(self):
		self.gui.clear()
		self.load()

	def draw(self):
		self.batch.draw()
		self.gui.batch.draw()

	def run(self, dt):
		if not self.paused:
			if self.world.state == WorldStates.POST_LAUNCH:
				for i in range(self.simulation_speed):
					self.world.step(dt*200)

		if DEBUG:
			self.offset_line.x2, self.offset_line.y2 = self.camera.to_screen_space(*self.world.planets[0].pos)
			self.mouse_line.x2, self.mouse_line.y2 = self.camera.to_world_space(self.mouse_x, self.mouse_y)

	# Game logic

	def launch_ship(self):
		self.world.launch_ship()
		self.graph.unhide()

	def reset(self):
		self.time_slider.reset()
		self.graph.reset()
		self.graph.hide()
		self.load_level()
