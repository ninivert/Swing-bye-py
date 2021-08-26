import pyglet
import numpy as np
import json
import logging
from swingbye.levels.parser import parse_level
from swingbye.physics.world import WorldStates
from swingbye.pygletengine.components.overlays import Options
from swingbye.pygletengine.utils import point_in_rect, create_sprite
from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.scenes.layers.camera import Camera
from swingbye.pygletengine.gameobjects.backgroundobject import BackgroundObject
from swingbye.pygletengine.gameobjects.hudobject import HudObject
from swingbye.pygletengine.globals import WINDOW_WIDTH, WINDOW_HEIGHT, DEBUG_CAMERA, DEBUG_COLLISION, GameState, GameEntity
from swingbye.pygletengine.components.paths import PointPath, LinePath
from swingbye.pygletengine.gameobjects.entities import ShipObject, PlanetObject
from swingbye.globals import PLANET_PREDICTION_N, SHIP_PREDICTION_N, PHYSICS_DT

_logger = logging.getLogger(__name__)


class Editor(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.register_event_type('on_win')
		self.register_event_type('on_lose')
		self.register_event_type('on_reset')

		self.level = 'swingbye/levels/main_menu.json'

		self.planet_sprites = [
			'assets/sprites/planet1.png',
			'assets/sprites/planet2.png',
			'assets/sprites/planet3.png',
			'assets/sprites/planet4.png',
			'assets/sprites/planet5.png'
		]

		self.game_state = GameState.RUNNING
		self.simulation_speed = 1

		# TODO : cleanup this
		self.mouse_press_x = 0
		self.mouse_press_y = 0

		self.mouse_x = 0
		self.mouse_y = 0

	# WHY DOESNT THIS WORK??????
	def on_file_drop(self, x, y, file):
		print(file)

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
		if self.hud.is_over(x, y):
			self.hud.on_mouse_press(x, y, buttons, modifiers)

	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.game_state == GameState.RUNNING:
			clicked = self.mouse_press_x == x and self.mouse_press_y == y
			if not self.hud.is_over(x, y):
				if clicked:
					self.add_planet()
					# self.world.point_ship(self.camera.screen_to_world(x, y))

		self.hud.on_mouse_release(x, y, buttons, modifiers)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if self.game_state == GameState.RUNNING:
			if not self.hud.is_over(x, y):
				if scroll_y != 0:
					self.camera.zoom_at(x, y, scroll_y)

	def on_resize(self, width, height):
		self.hud_rect = self.hud.rect
		self.background.on_resize(width, height)
		self.camera.on_resize(width, height)

	def on_option_change(self, name, value):
		pass

	def on_confirm(self, options):
		print(options)
		self.hud.container.remove(self.planet_options)
		planetobject = PlanetObject(
			sprite=create_sprite(self.planet_sprites[0], subpixel=True, batch=self.world_batch, group=pyglet.graphics.OrderedGroup(0, parent=self.world_group)),
			# TODO: colors
			path=PointPath(batch=self.world_batch, fade=True, point_count=PLANET_PREDICTION_N),
			parent=self.world.planets[0],
			# TODO : named planets
			# name=child_dict['name'],
			game_entity=GameEntity.PLANET,
			**options
		)
		self.world.planets.append(planetobject)
		self.world.time = 0

	def on_speed_change(self, widget, value):
		self.simulation_speed = int(value)
		self.hud.graph.sample_rate = 1/10 / int(value)

	def on_time_change(self, widget, value):
		self.world.time = value

	def on_pause(self):
		self.game_state = GameState.PAUSED
		self.hud.graph.pause_sampling()
		self.hud.pause_menu.open(self.gui)

	def on_resume(self):
		self.game_state = GameState.RUNNING
		self.hud.pause_menu.close()
		self.hud.graph.resume_sampling()

	def on_win(self):
		self.game_state = GameState.ENDING
		self.hud.pause_sampling()
		self.hud.on_win()

	def on_lose(self):
		self.game_state = GameState.ENDING
		self.hud.graph.pause_sampling()
		self.hud.on_lose()

	def on_reset(self):
		self.reset()

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

		self.entity_label = pyglet.text.Label('AAAAAAA', batch=self.world_batch, group=pyglet.graphics.OrderedGroup(1, parent=self.world_group))

		self.hud_rect = self.hud.rect

	def load_level(self):
		with open(self.level) as file:
			level = json.load(file)

		self.background = BackgroundObject(
			level['background_sprite'],
			self.camera,
			self.batch,
			self.background_group
		)

		self.world = parse_level(level, self.world_batch, self.world_group)

	def load(self):
		self.batch = pyglet.graphics.Batch()
		self.world_batch = pyglet.graphics.Batch()

		self.background_group = pyglet.graphics.OrderedGroup(0)
		self.world_group = pyglet.graphics.OrderedGroup(1)
		self.foreground_group = pyglet.graphics.OrderedGroup(2)

		self.camera = Camera(self.window)

		self.load_level()
		self.load_hud()

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
		# self.background.update()

		if self.game_state == GameState.RUNNING:
			if self.world.state == WorldStates.POST_LAUNCH:
				for i in range(self.simulation_speed):
					self.world.step(PHYSICS_DT)

					# Check collisions
					for planet in self.world.planets:
						if self.world.ship.collides_with(planet):
							if planet.game_entity == GameEntity.PLANET:
								self.dispatch_event('on_lose')
							elif planet.game_entity == GameEntity.WORMHOLE:
								self.dispatch_event('on_win')

	def add_planet(self):
		options_dict = {
			# Semi-major axis
			'maxis': {'type': 'slider', 'min_value': 1, 'max_value': 1000, 'step': 1, 'default': 1.0},
			# Eccentricity
			'ecc': {'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': 0.0},
			# Initial time offset
			'time0': {'type': 'slider', 'min_value': 0, 'max_value': 50000, 'step': 5, 'default': 0.0},
			# Inclination
			'incl': {'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': 0.0},
			# Argument of periaxis
			'parg': {'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': 0.0},
			# Planet radius
			'radius': {'type': 'slider', 'min_value': 0, 'max_value': 100, 'step': 1, 'default': 10},
			# Mass
			'mass': {'type': 'slider', 'min_value': 1, 'max_value': 1000, 'step': 1, 'default': 1}
		}
		self.planet_options = Options(options_dict)
		self.planet_options.set_handler('on_option_change', self.on_option_change)
		self.planet_options.set_handler('on_confirm', self.on_confirm)
		self.hud.container.add(self.planet_options, left=10, bottom=50)

	def launch_ship(self):
		self.world.launch_ship()
		self.hud.show_graph()

	def reset(self):
		self.hud.reset()
		self.hud.hide_graph()

		# This is very bad, old objects are not getting cleaned up (sprites need to be removed from batches etc)
		# When reset is spammed, memory usage increases greatly
		# TODO -= 1  # yay
		self.load_level()
