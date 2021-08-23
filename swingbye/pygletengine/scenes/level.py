import pyglet
import glooey
import numpy as np
import json
import logging
from .scene import Scene
from .layers.parallax import ParallaxGroup
from .layers.camera import Camera
from ..utils import create_sprite, clamp, point_in_rect
from ..gameobjects.pointpath import PointPath
from ..gameobjects.linepath import LinePath
from ...physics.ship import Ship
from ...physics.world import World, WorldStates
from ...physics.integrator import EulerIntegrator, RK4Integrator
from ..gameobjects.planetobject import PlanetObject
from ..gameobjects.shipobject import ShipObject
from ..gameobjects.starobject import StarObject
from ..gameobjects.backgroundobject import BackgroundObject
from ..gameobjects.hudobject import HudObject
from ..globals import WINDOW_WIDTH, WINDOW_HEIGHT, DEBUG_CAMERA, GameState
from ...globals import PLANET_PREDICTION_N, SHIP_PREDICTION_N, PHYSICS_DT

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
		self.game_state = GameState.RUNNING

		self.mouse_x = 0
		self.mouse_y = 0

	def on_mouse_motion(self, x, y, dx, dy):
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.game_state == GameState.RUNNING:
			if self.hud.captured:
				self.hud.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
			else:
				self.camera.move(-dx, -dy)
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_press(self, x, y, buttons, modifiers):
		self.mouse_press_x = x
		self.mouse_press_y = y

	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.game_state == GameState.RUNNING:
			clicked = self.mouse_press_x == x and self.mouse_press_y == y
			if not point_in_rect(x, y, *self.hud_rect.bottom_left, *self.hud_rect.size):
				if clicked:
					self.world.point_ship(self.camera.screen_to_world(x, y))

		self.hud.on_mouse_release(x, y, buttons, modifiers)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if self.game_state == GameState.RUNNING:
			if not point_in_rect(x, y, *self.hud_rect.bottom_left, *self.hud_rect.size):
				if scroll_y != 0:
					self.camera.zoom_at(x, y, scroll_y)

	def on_resize(self, width, height):
		self.hud_rect = self.hud.rect
		self.background.on_resize(width, height)
		self.camera.on_resize(width, height)

	def on_speed_change(self, value):
		self.simulation_speed = int(value)
		self.hud.graph.sample_rate = 1/10 / int(value)

	def on_time_change(self, value):
		self.world.time = value

	def on_pause(self):
		self.game_state = GameState.PAUSED
		self.hud.pause_menu.open(self.gui)
		self.hud.graph.pause_sampling()
	
	def on_resume(self):	
		self.game_state = GameState.RUNNING
		self.hud.pause_menu.close()
		self.hud.graph.resume_sampling()

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
					sprite=create_sprite(child_dict['sprite'], subpixel=True, batch=batch, group=group),
					# TODO: colors
					path=PointPath(batch=batch, point_count=PLANET_PREDICTION_N),
					# TODO : named planets
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
					sprite=create_sprite(child_dict['sprite'], subpixel=True, batch=batch, group=group),
					path=LinePath(batch=batch, point_count=SHIP_PREDICTION_N),
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
		self.hud = HudObject(self.gui)

		self.hud.reset_button.set_handler('on_press', self.reset)
		self.hud.pause_button.set_handler('on_press', self.on_pause)
		self.hud.speed_slider.set_handler('on_change', self.on_speed_change)
		self.hud.time_slider.set_handler('on_change', self.on_time_change)
		self.hud.launch_button.set_handler('on_press', self.launch_ship)

		self.hud.pause_menu.resume_button.set_handler('on_press', self.on_resume)
		self.hud.pause_menu.quit_button.set_handler('on_press', pyglet.app.exit)

		self.hud.graph.query = lambda: np.linalg.norm(self.world.ship.vel)
		self.hud.hide_graph()

		self.hud_rect = self.hud.rect

	def load_level(self):
		with open(self.levels[self.level_index]) as file:
			level = json.load(file)

		self.background = BackgroundObject(
			level['background_sprite'],
			self.camera,
			self.batch,
			self.background_group,
			layers=self.tmp_parallax_layers
		)

		_logger.debug(f'parsing level from file `{self.levels[self.level_index]}`')

		self.world = self.parse_level(level, self.world_batch, self.world_group)

	def load(self):
		self.batch = pyglet.graphics.Batch()
		self.world_batch = pyglet.graphics.Batch()

		self.background_group = pyglet.graphics.OrderedGroup(3)
		self.world_group = pyglet.graphics.OrderedGroup(4)
		self.foreground_group = pyglet.graphics.OrderedGroup(5)

		# TODO: find a way to put this in the background object
		# such that it doesn't break when reset
		# I believe the issues comes from recreating a group with the same order
		# whilst the old one is still in memory somewhere
		self.tmp_parallax_layers = [
			ParallaxGroup(i, rate=1/(i+6)**2) for i in range(3)
		]

		self.camera = Camera(self.window)

		if DEBUG_CAMERA:
			self.offset_line = pyglet.shapes.Line(0, 0, 0, 0, color=(255, 20, 20), batch=self.batch, group=self.foreground_group)
			self.mouse_line = pyglet.shapes.Line(0, 0, 0, 0, color=(20, 255, 20), batch=self.world_batch, group=self.foreground_group)
			self.mouse_world_to_screen_line = pyglet.shapes.Line(0, 0, 0, 0, color=(255, 255, 20), batch=self.batch, group=self.foreground_group)

		self.load_level()
		self.load_hud()

		self.camera.set_parent(self.world.ship)

	def begin(self):
		self.gui.clear()
		self.load()

	def draw(self):
		self.batch.draw()
		with self.camera:
			self.world_batch.draw()
		self.gui.batch.draw()

	def run(self, dt):
		# TODO: find a way to update the camera here instead of before drawing (make it independent of fps)
		# self.camera.update()
		self.background.update()

		if self.game_state == GameState.RUNNING:
			if self.world.state == WorldStates.POST_LAUNCH:
				for i in range(self.simulation_speed):
					self.world.step(PHYSICS_DT)

		if DEBUG_CAMERA:
			# WARNING: lines are always late by 1 frame
			# do not trust them too much on fast moving entities
			self.offset_line.x2, self.offset_line.y2 = self.camera.world_to_screen(*self.world.planets[0].pos)
			self.mouse_line.x2, self.mouse_line.y2 = self.camera.screen_to_world(self.mouse_x, self.mouse_y)
			self.mouse_world_to_screen_line.x2, self.mouse_world_to_screen_line.y2 = self.camera.world_to_screen(*self.camera.screen_to_world(self.mouse_x, self.mouse_y))

	# Game logic

	def launch_ship(self):
		self.world.launch_ship()
		self.hud.show_graph()

	def reset(self):
		self.hud.reset()
		self.hud.hide_graph()
		self.camera.set_parent(None)

		# This is very bad, old objects are not getting cleaned up (sprites need to be removed from batches etc)
		# When reset is spammed, memory usage increases greatly
		# TODO : cleanup this because it reconstructs the HUD, very overkill such excess
		self.load()
		self.camera.set_parent(self.world.ship)
