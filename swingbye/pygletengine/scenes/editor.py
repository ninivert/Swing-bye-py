import pyglet
import json
import logging
from swingbye.levels.parser import parse_level
from swingbye.logic.world import WorldStates
from swingbye.logic.collisions import HitZonePoint
from swingbye.pygletengine.components.overlays import OptionsOverlay
from swingbye.pygletengine.utils import point_in_rect, create_sprite
from swingbye.pygletengine.scenes.level import Level
from swingbye.pygletengine.scenes.layers.camera import Camera
from swingbye.pygletengine.gameobjects.backgroundobject import BackgroundObject
from swingbye.pygletengine.gameobjects.hudobject import HudObject
from swingbye.pygletengine.globals import WINDOW_WIDTH, WINDOW_HEIGHT, DEBUG_CAMERA, DEBUG_COLLISION, GameState, GameEntity, EditorState
from swingbye.pygletengine.components.paths import PointPath, LinePath
from swingbye.pygletengine.components.buttons import Button
from swingbye.pygletengine.gameobjects.entities import ShipObject, PlanetObject
from swingbye.globals import PLANET_PREDICTION_N, SHIP_PREDICTION_N, PHYSICS_DT

_logger = logging.getLogger(__name__)


class Editor(Level):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.register_event_type('on_win')
		self.register_event_type('on_lose')
		self.register_event_type('on_reset')

		self.levels = ['swingbye/levels/editor_test.json']

		self.sprites = {
			'Planet 1': 'assets/sprites/planet1.png',
			'Planet 2': 'assets/sprites/planet2.png',
			'Planet 3': 'assets/sprites/planet3.png',
			'Planet 4': 'assets/sprites/planet4.png',
			'Planet 5': 'assets/sprites/planet5.png',
			'Star 1': 'assets/sprites/star1.png',
			'Star 2': 'assets/sprites/star2.png',
			'Star 3': 'assets/sprites/star3.png',
			'Fire comet': 'assets/sprites/comete_feu.png',
			'Ice comet': 'assets/sprites/comete_glace.png',
			'Rock comet': 'assets/sprites/comete_roche.png'
		}
		self.selected_planet_index = -1

		self.planet_defaults = {
			# Sprite
			'sprite': 'Planet 1',
			# Control values
			'kwargs': {
				# Semi-major axis
				'maxis': 100,
				# Eccentricity
				'ecc': 0.0,
				# Initial time offset
				'time0': 0.0,
				# Inclination
				'incl': 0.0,
				# Argument of periaxis
				'parg': 0.0,
				# Planet radius
				'radius': 10,
				# Mass{'description': 'Sprite',
				'mass': 1
			}
		}

		self.state = EditorState.NOTHING
		self.menu = None

	# WHY DOESNT THIS WORK??????
	def on_file_drop(self, x, y, file):
		print(file)

	def on_click(self, x, y):
		if self.game_state == GameState.RUNNING:
			if not self.hud.is_over(x, y):
				if self.is_over_planet(x, y):
					planet, index = self.get_planet_at(x, y)
					self.select_planet(index)
					self.open_edit_context_menu(self.world.planets[self.selected_planet_index])

	def on_option_change(self, name, value):
		self.edit_planet(self.selected_planet_index, name, value)

	def on_delete(self):
		self.delete_planet(self.selected_planet_index)
		self.deselect_planet()

	def on_confirm(self):
		self.confirm_change()

	def on_cancel(self):
		self.cancel_change()

	def on_add(self):
		# HACK
		self.add_planet(self.sprites[self.planet_defaults['sprite']], self.world.planets[self.selected_planet_index], self.planet_defaults['kwargs'])
		self.select_planet(len(self.world.planets) - 1)
		self.open_add_context_menu()

	def draw(self):
		self.batch.draw()
		with self.camera:
			self.world_batch.draw()
			if self.selected_planet_index != -1:
				glow = pyglet.shapes.Circle(*self.world.planets[self.selected_planet_index].pos, self.world.planets[self.selected_planet_index].radius, color=(220, 189, 122))
				glow.opacity = 128
				glow.draw()
		self.gui.batch.draw()

	def close_context_menus(self):
		if self.state == EditorState.EDITING:
			self.hud.close_overlay('edit_planet')
		if self.state == EditorState.ADDING:
			self.hud.close_overlay('add_planet')

	def cancel_change(self):
		self.close_context_menus()
		if self.state == EditorState.EDITING:
			# TODO: cancel changes...
			pass
		if self.state == EditorState.ADDING:
			self.world.planets[self.selected_planet_index].delete()
			self.world.planets.pop(self.selected_planet_index)
		self.state = EditorState.NOTHING
		self.deselect_planet()

	def confirm_change(self):
		# HACK: send back options in arguments
		if self.state == EditorState.EDITING:
			self.hud.close_overlay('edit_planet')
			options = self.hud.overlays['edit_planet'].option_values
			for name in options.keys():
				self.edit_planet(self.selected_planet_index, name, options[name])

		if self.state == EditorState.ADDING:
			self.hud.close_overlay('add_planet')
			options = self.hud.overlays['add_planet'].option_values

			sprite = options.pop('sprite')

			self.world.planets[self.selected_planet_index].delete()
			planet = self.create_planet(sprite, self.world.planets[self.selected_planet_index].parent, options)
			self.world.planets[self.selected_planet_index] = planet

		self.world.time = self.world.time
		self.state = EditorState.NOTHING
		self.deselect_planet()

	def open_edit_context_menu(self, planet):
		self.close_context_menus()
		options_dict = {
			# Sprite
			# TODO: set default to planet sprite
			# TODO: fix cycle button when changing default value
			# TODO: clean up these todos lol
			'sprite': {'description': 'Sprite', 'type': 'cycle', 'states': self.sprites, 'default': 'Planet 1'},
			# Semi-major axis
			'maxis': {'description': 'Distance', 'type': 'slider', 'min_value': 1, 'max_value': 5000, 'step': 1, 'default': planet.maxis},
			# Eccentricity
			'ecc': {'description': 'Eccentricity', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': planet.ecc},
			# Initial time offset
			'time0': {'description': 'Time offset', 'type': 'slider', 'min_value': 0, 'max_value': 50000, 'step': 5, 'default': planet.time0},
			# Inclination
			'incl': {'description': 'Inclination', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': planet.incl},
			# Argument of periaxis
			'parg': {'description': 'Something parg', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': planet.parg},
			# Planet radius
			'radius': {'description': 'Radius', 'type': 'slider', 'min_value': 0, 'max_value': 500, 'step': 1, 'default': planet.radius},
			# Mass{'description': 'Sprite',
			'mass': {'description': 'Mass', 'type': 'slider', 'min_value': 1, 'max_value': 1000, 'step': 1, 'default': planet.mass},
			# Add child
			'add_child': {'description': '', 'type': 'button', 'label': 'Add child', 'callback': self.on_add, 'default': None},
			# Delete
			'delete': {'description': '', 'type': 'button', 'label': 'Delete planet', 'callback': self.on_delete, 'default': None},
			# Confirm changes
			'confirm': {'description': '', 'type': 'button', 'label': 'Confirm', 'callback': self.on_confirm, 'default': None},
			# Cancel
			'cancel': {'description': '', 'type': 'button', 'label': 'Cancel', 'callback': self.on_cancel, 'default': None}
		}
		# TODO: planet name as title
		self.menu = OptionsOverlay('Edit {NAME}', options_dict)
		# Kinda hacky because should work without, but eh
		self.menu.set_handler('on_option_change', self.on_option_change)
		self.hud.add_overlay('edit_planet', self.menu)
		self.hud.open_overlay('edit_planet', left=10, bottom=50)
		self.state = EditorState.EDITING

	def open_add_context_menu(self):
		self.close_context_menus()
		options_dict = {
			# Sprite
			'sprite': {'description': 'Sprite', 'type': 'cycle', 'states': self.sprites, 'default': self.planet_defaults['sprite']},
			# Semi-major axis
			'maxis': {'description': 'Distance', 'type': 'slider', 'min_value': 1, 'max_value': 5000, 'step': 1, 'default': self.planet_defaults['kwargs']['maxis']},
			# Eccentricity
			'ecc': {'description': 'Eccentricity', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': self.planet_defaults['kwargs']['ecc']},
			# Initial time offset
			'time0': {'description': 'Time offset', 'type': 'slider', 'min_value': 0, 'max_value': 50000, 'step': 5, 'default': self.planet_defaults['kwargs']['time0']},
			# Inclination
			'incl': {'description': 'Inclination', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': self.planet_defaults['kwargs']['incl']},
			# Argument of periaxis
			'parg': {'description': 'Something parg', 'type': 'slider', 'min_value': 0, 'max_value': 1, 'step': 0.01, 'default': self.planet_defaults['kwargs']['parg']},
			# Planet radius
			'radius': {'description': 'Radius', 'type': 'slider', 'min_value': 0, 'max_value': 500, 'step': 1, 'default': self.planet_defaults['kwargs']['radius']},
			# Mass{'description': 'Sprite',
			'mass': {'description': 'Mass', 'type': 'slider', 'min_value': 1, 'max_value': 1000, 'step': 1, 'default': self.planet_defaults['kwargs']['mass']},
			# Confirm adding button
			'confirm': {'description': '', 'type': 'button', 'label': 'Confirm', 'callback': self.on_confirm, 'default': None},
			# Cancel button
			'cancel': {'description': '', 'type': 'button', 'label': 'Cancel', 'callback': self.on_cancel, 'default': None}
		}
		self.menu = OptionsOverlay('Create a planet', options_dict)
		self.menu.set_handler('on_option_change', self.on_option_change)
		self.hud.add_overlay('add_planet', self.menu)
		self.hud.open_overlay('add_planet', left=10, bottom=50)
		self.state = EditorState.ADDING

	def edit_planet(self, index, name, value):
		if name == 'sprite':
			image = pyglet.resource.image(value)
			image.anchor_x = image.width // 2
			image.anchor_y = image.height // 2
			self.world.planets[index].sprite.image = image
			# Update the scaling for radius
			self.world.planets[index].sprite.scale = 1
			scale = self.world.planets[index].radius / (self.world.planets[index].sprite.height//2)
			self.world.planets[index].sprite.scale = scale
		if name == 'maxis':
			self.world.planets[index].maxis = value
		if name == 'ecc':
			self.world.planets[index].ecc = value
		if name == 'time0':
			self.world.planets[index].time0 = value
		if name == 'incl':
			self.world.planets[index].incl = value
		if name == 'parg':
			self.world.planets[index].parg = value
		if name == 'radius':
			self.world.planets[index].radius = value
			self.world.planets[index].sprite.scale = 1
			scale = value / (self.world.planets[index].sprite.height//2)
			self.world.planets[index].sprite.scale = scale
		if name == 'mass':
			self.world.planets[index].mass = value

		# HACK: need a world.update function
		self.world.time = self.world.time

	def create_planet(self, sprite, parent, options):
		planet = PlanetObject(
			sprite=create_sprite(sprite, subpixel=True, batch=self.world_batch, group=pyglet.graphics.OrderedGroup(0, parent=self.world_group)),
			# TODO: colors
			path=PointPath(batch=self.world_batch, fade=True, point_count=PLANET_PREDICTION_N),
			parent=parent,
			# TODO : named planets
			# name=child_dict['name'],
			game_entity=GameEntity.PLANET,
			**options
		)
		return planet

	def add_planet(self, sprite, parent, options):
		planet = self.create_planet(sprite, parent, options)
		self.world.planets.append(planet)

		# HACK: need a world.update function
		self.world.time = self.world.time

	def delete_planet(self, index):
		self.world.planets[index].delete()
		self.world.planets.pop(index)
		self.hud.close_overlay('edit_planet')
		self.deselect_planet()

	def select_planet(self, index):
		self.selected_planet_index = index

	def deselect_planet(self):
		self.selected_planet_index = -1

	def save(self):
		data = {
			"title": "title",
			"description": "description",
			"background_sprite": "assets/bg3.png",
			"world": []
		}
		
		# https://stackoverflow.com/questions/7523920/converting-a-parent-child-relationship-into-json-in-python
		world = {'planet': None}
		lookup = {None: world}
		for planet in self.world.planets:
			# if planet.parent is None:
			# 	world['children'].append('planet')
			# 	lookup[planet] = world
			# else:
			node = {'planet': planet}
			lookup[planet.parent].setdefault('children', []).append(node)
			lookup[planet] = node

		def convert(planet):
			data = {}
			data['type'] = 'planet' if planet['planet'].game_entity == GameEntity.PLANET else 'wormhole'
			# TODO: save sprite
			data['sprite'] = self.sprites[self.planet_defaults['sprite']]
			# TODO: planet names
			data['name'] = ''
			data['arguments'] = {}
			data['arguments']['maxis'] = planet['planet'].maxis
			data['arguments']['ecc'] = planet['planet'].ecc
			data['arguments']['time0'] = planet['planet'].time0
			data['arguments']['incl'] = planet['planet'].incl
			data['arguments']['parg'] = planet['planet'].parg
			data['arguments']['radius'] = planet['planet'].radius
			data['arguments']['mass'] = planet['planet'].mass
			data['arguments']['anchor'] = list(planet['planet'].anchor)
			data['children'] = [convert(child) for child in planet.get('children', [])]
			return data

		for planet in world['children']:
			data['world'].append(convert(planet))

		with open('swingbye/levels/editor_test.json', 'w') as file:
			json.dump(data, file)

	def load_hud(self):
		super().load_hud()
		# Avoid having the button gc'ed
		save_button = Button('Save', callback=self.save)
		self.hud.overlays['pause'].container.add(save_button)

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
		super().reset()
		self.camera.set_parent(None)
