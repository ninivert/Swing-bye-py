import pyglet
import numpy as np
import json
import logging
from swingbye.levels.parser import parse_level
from swingbye.physics.world import WorldStates
from swingbye.physics.collisions import HitZonePoint
from swingbye.pygletengine.components.overlays import OptionsOverlay
from swingbye.pygletengine.utils import point_in_rect, create_sprite
from swingbye.pygletengine.scenes.level import Level
from swingbye.pygletengine.scenes.layers.camera import Camera
from swingbye.pygletengine.gameobjects.backgroundobject import BackgroundObject
from swingbye.pygletengine.gameobjects.hudobject import HudObject
from swingbye.pygletengine.globals import WINDOW_WIDTH, WINDOW_HEIGHT, DEBUG_CAMERA, DEBUG_COLLISION, GameState, GameEntity, EditorState
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
		self.selected_planet_index = 0
		
		self.editor_state = EditorState.NOTHING

	# WHY DOESNT THIS WORK??????
	def on_file_drop(self, x, y, file):
		print(file)

	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.game_state == GameState.RUNNING:
			clicked = self.mouse_press_x == x and self.mouse_press_y == y
			if not self.hud.is_over(x, y):
				if self.is_over_planet(x, y):
					self.select_planet(x, y)

		self.hud.on_mouse_release(x, y, buttons, modifiers)

	def on_option_change(self, name, value):
		if name == 'sprite':
			image = pyglet.resource.image(value)
			image.anchor_x = image.width // 2
			image.anchor_y = image.height // 2
			self.world.planets[self.selected_planet_index].sprite.image = image
		if name == 'maxis':
			self.world.planets[self.selected_planet_index].maxis = value
		if name == 'ecc':
			self.world.planets[self.selected_planet_index].ecc = value
		if name == 'time0':
			self.world.planets[self.selected_planet_index].time0 = value
		if name == 'incl':
			self.world.planets[self.selected_planet_index].incl = value
		if name == 'parg':
			self.world.planets[self.selected_planet_index].parg = value
		if name == 'radius':
			self.world.planets[self.selected_planet_index].radius = value
		if name == 'mass':
			self.world.planets[self.selected_planet_index].mass = value
		# HACK: need a world.update function
		self.world.time = self.world.time

	def on_confirm(self):
		options = self.hud.overlays['add_planet'].option_values
		self.hud.close_overlay('add_planet')
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
		self.world.time = self.world.time
		self.editor_state = EditorState.NOTHING
		self.deselect_planet()

	def on_cancel(self):
		if self.editor_state == EditorState.EDITING:
			self.hud.close_overlay('edit_planet')
		if self.editor_state == EditorState.ADDING:
			self.hud.close_overlay('add_planet')
			self.world.planets.pop(len(self.world.planets)-1)
		self.world.time = self.world.time
		self.editor_state = EditorState.NOTHING
		self.deselect_planet()

	def draw(self):
		self.batch.draw()
		with self.camera:
			self.world_batch.draw()
			if self.selected_planet is not None:
				glow = pyglet.shapes.Circle(*self.selected_planet.pos, self.selected_planet.radius, color=(220, 189, 122))
				glow.opacity = 128
				glow.draw()
		self.gui.batch.draw()

	def edit_planet(self):
		options_dict = {
			# Sprite
			'sprite': {'description': 'Sprite', 'type': 'cycle', 'states': self.planet_sprites, 'default': self.planet_sprites['Planet 1']},
			# Semi-major axis
			'maxis': {'description': 'Distance', 'type': 'slider', 'min_value': 1, 'max_value': 5000, 'step': 1, 'default': self.selected_planet.maxis},
			# Eccentricity
			'ecc': {'description': 'Eccentricity', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': self.selected_planet.ecc},
			# Initial time offset
			'time0': {'description': 'Time offset', 'type': 'slider', 'min_value': 0, 'max_value': 50000, 'step': 5, 'default': self.selected_planet.time0},
			# Inclination
			'incl': {'description': 'Inclination', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': self.selected_planet.incl},
			# Argument of periaxis
			'parg': {'description': 'Something parg', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': self.selected_planet.parg},
			# Planet radius
			'radius': {'description': 'Radius', 'type': 'slider', 'min_value': 0, 'max_value': 500, 'step': 1, 'default': self.selected_planet.radius},
			# Mass{'description': 'Sprite', 
			'mass': {'description': 'Mass', 'type': 'slider', 'min_value': 1, 'max_value': 1000, 'step': 1, 'default': self.selected_planet.mass},
			# Add child
			'add_child': {'description': '', 'type': 'button', 'label': 'Add child', 'callback': self.add_planet},
			# Delete
			'delete': {'description': '', 'type': 'button', 'label': 'Delete planet', 'callback': self.delete_planet},
			# Cancel
			'cancel': {'description': '', 'type': 'button', 'label': 'Cancel', 'callback': self.on_cancel}
		}
		self.editor = OptionsOverlay('Edit planet', options_dict)
		self.hud.add_overlay('edit_planet', self.editor)
		self.hud.open_overlay('edit_planet', left=10, bottom=50)
		self.editor_state = EditorState.EDITING

	def add_planet(self):
		self.hud.close_overlay('edit_planet')

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
			'sprite': {'description': 'Sprite', 'type': 'cycle', 'states': self.planet_sprites, 'default': self.planet_sprites['Planet 1']},
			# Semi-major axis
			'maxis': {'description': 'Distance', 'type': 'slider', 'min_value': 1, 'max_value': 5000, 'step': 1, 'default': 100},
			# Eccentricity
			'ecc': {'description': 'Eccentricity', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': 0.0},
			# Initial time offset
			'time0': {'description': 'Time offset', 'type': 'slider', 'min_value': 0, 'max_value': 50000, 'step': 5, 'default': 0.0},
			# Inclination
			'incl': {'description': 'Inclination', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': 0.0},
			# Argument of periaxis
			'parg': {'description': 'Something parg', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': 0.0},
			# Planet radius
			'radius': {'description': 'Radius', 'type': 'slider', 'min_value': 0, 'max_value': 500, 'step': 1, 'default': 10},
			# Mass{'description': 'Sprite', 
			'mass': {'description': 'Mass', 'type': 'slider', 'min_value': 1, 'max_value': 1000, 'step': 1, 'default': 1},
			# Confirm adding button
			'confirm': {'description': '', 'type': 'button', 'label': 'Confirm', 'callback': self.on_confirm},
			# Cancel button
			'cancel': {'description': '', 'type': 'button', 'label': 'Cancel', 'callback': self.on_cancel}
		}
		self.editor = OptionsOverlay('Create a planet', options_dict)

		self.hud.add_overlay('add_planet', self.editor)
		self.hud.open_overlay('add_planet', left=10, bottom=50)
		self.editor_state = EditorState.ADDING

	def delete_planet(self):
		self.world.planets.pop(self.selected_planet_index)
		self.hud.close_overlay('edit_planet')
		self.deselect_planet()

	def select_planet(self, x, y):
		self.selected_planet, self.selected_planet_index = self.get_planet_at(x, y)
		self.edit_planet()

	def deselect_planet(self):
		self.selected_planet = None
		self.selected_planet_index = 0

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
		for index, planet in enumerate(self.world.planets):
			if planet.collides_with(pos):
				return planet, index
		return None, 0

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
