import pyglet
import numpy as np
import json
import logging
from swingbye.levels.parser import parse_level
from swingbye.physics.world import WorldStates
from swingbye.physics.collisions import HitZonePoint
from swingbye.pygletengine.components.overlays import Options
from swingbye.pygletengine.utils import point_in_rect, create_sprite
from swingbye.pygletengine.scenes.level import Level
from swingbye.pygletengine.scenes.layers.camera import Camera
from swingbye.pygletengine.gameobjects.backgroundobject import BackgroundObject
from swingbye.pygletengine.gameobjects.hudobject import HudObject
from swingbye.pygletengine.globals import WINDOW_WIDTH, WINDOW_HEIGHT, DEBUG_CAMERA, DEBUG_COLLISION, GameState, GameEntity
from swingbye.pygletengine.components.paths import PointPath, LinePath
from swingbye.pygletengine.gameobjects.entities import ShipObject, PlanetObject
from swingbye.globals import PLANET_PREDICTION_N, SHIP_PREDICTION_N, PHYSICS_DT

_logger = logging.getLogger(__name__)


class Editor(Level):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.register_event_type('on_win')
		self.register_event_type('on_lose')
		self.register_event_type('on_reset')

		self.levels = ['swingbye/levels/main_menu.json']

		self.planet_sprites = {
			'Planet 1': 'assets/sprites/planet1.png',
			'Planet 2': 'assets/sprites/planet2.png',
			'Planet 3': 'assets/sprites/planet3.png',
			'Planet 4': 'assets/sprites/planet4.png',
			'Planet 5': 'assets/sprites/planet5.png'
		}
		self.selected_planet = None
		self.adding_planet = False

	# WHY DOESNT THIS WORK??????
	def on_file_drop(self, x, y, file):
		print(file)

	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.game_state == GameState.RUNNING:
			clicked = self.mouse_press_x == x and self.mouse_press_y == y
			if not self.hud.is_over(x, y):
				if self.is_over_planet(x, y):
					self.select_planet(x, y)
				else:
					if clicked:
						if not self.adding_planet:
							self.add_planet()
							self.adding_planet = True
						# self.world.point_ship(self.camera.screen_to_world(x, y))

		self.hud.on_mouse_release(x, y, buttons, modifiers)

	def on_option_change(self, name, value):
		if name == 'sprite':
			image = pyglet.resource.image(value)
			image.anchor_x = image.width // 2
			image.anchor_y = image.height // 2
			self.world.planets[-1].sprite.image = image
		if name == 'maxis':
			self.world.planets[-1].maxis = value
		if name == 'ecc':
			self.world.planets[-1].ecc = value
		if name == 'time0':
			self.world.planets[-1].time0 = value
		if name == 'incl':
			self.world.planets[-1].incl = value
		if name == 'parg':
			self.world.planets[-1].parg = value
		if name == 'radius':
			self.world.planets[-1].radius = value
		if name == 'mass':
			self.world.planets[-1].mass = value
		self.world.time = 1

	def on_confirm(self, options):
		self.hud.container.remove(self.planet_options)
		sprite = options.pop('sprite')

		planetobject = PlanetObject(
			sprite=create_sprite(sprite, subpixel=True, batch=self.world_batch, group=pyglet.graphics.OrderedGroup(0, parent=self.world_group)),
			# TODO: colors
			path=PointPath(batch=self.world_batch, fade=True, point_count=PLANET_PREDICTION_N),
			parent=self.selected_planet,
			# TODO : named planets
			# name=child_dict['name'],
			game_entity=GameEntity.PLANET,
			**options
		)
		self.world.planets[-1] = planetobject
		self.world.time = 0
		self.adding_planet = False

	def on_cancel(self):
		self.hud.container.remove(self.planet_options)
		self.world.planets.pop(len(self.world.planets)-1)
		self.world.time = 0
		self.adding_planet = False

	def draw(self):
		self.batch.draw()
		with self.camera:
			self.world_batch.draw()
			if self.selected_planet is not None:
				glow = pyglet.shapes.Circle(*self.selected_planet.pos, self.selected_planet.radius, color=(220, 189, 122))
				glow.opacity = 128
				glow.draw()
		self.gui.batch.draw()

	def add_planet(self):
		planetobject = PlanetObject(
			sprite=create_sprite(self.planet_sprites['Planet 1'], subpixel=True, batch=self.world_batch, group=pyglet.graphics.OrderedGroup(0, parent=self.world_group)),
			# TODO: colors
			path=PointPath(batch=self.world_batch, fade=True, point_count=PLANET_PREDICTION_N),
			parent=self.selected_planet,
			# TODO : named planets
			# name=child_dict['name'],
			game_entity=GameEntity.PLANET,
		)
		self.world.planets.append(planetobject)

		options_dict = {
			# Sprite
			'sprite': {'type': 'cycle', 'states': self.planet_sprites, 'default': self.planet_sprites['Planet 1']},
			# Semi-major axis
			'maxis': {'type': 'slider', 'min_value': 1, 'max_value': 5000, 'step': 1, 'default': self.camera.screen_to_world(self.mouse_x, self.mouse_y)[0]},
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
		self.planet_options = Options('Create a planet', options_dict)
		self.planet_options.set_handler('on_option_change', self.on_option_change)
		self.planet_options.set_handler('on_confirm', self.on_confirm)
		self.planet_options.set_handler('on_cancel', self.on_cancel)
		self.hud.add_overlay('planet_options', self.planet_options)
		self.hud.open_overlay('planet_options', left=10, bottom=50)

	def select_planet(self, x, y):
		self.selected_planet = self.get_planet_at(x, y)

	def begin(self):
		self.gui.clear()
		self.load()
		self.camera.set_parent(None)

	def is_over_planet(self, x, y):
		mouse = HitZonePoint(self.camera.screen_to_world(x, y))
		for planet in self.world.planets:
			if planet.collides_with(mouse):
				return True
		return False

	def get_planet_at(self, x, y):
		pos = HitZonePoint(self.camera.screen_to_world(x, y))
		for planet in self.world.planets:
			if planet.collides_with(pos):
				return planet
		return None

	def launch_ship(self):
		# Hacky, but works
		self.world.state = WorldStates.POST_LAUNCH

	def reset(self):
		self.hud.reset()
		self.hud.hide_graph()

		# This is very bad, old objects are not getting cleaned up (sprites need to be removed from batches etc)
		# When reset is spammed, memory usage increases greatly
		# TODO -= 1  # yay
		self.load_level()
