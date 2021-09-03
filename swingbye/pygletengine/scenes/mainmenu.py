import pyglet
import json
import numpy as np
from pyglet.app import exit
from swingbye.levels.parser import parse_level
from swingbye.logic.collisions import HitZonePoint
from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.scenes.layers.camera import Camera
from swingbye.pygletengine.components.buttons import MainMenuButton
from swingbye.pygletengine.components.labels import Title
from swingbye.pygletengine.components.containers import Board, Around, Image
from swingbye.pygletengine.components.animation import Animation, Keyframe
from swingbye.pygletengine.gameobjects.backgroundobject import BackgroundObject
from swingbye.pygletengine.globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION


class MainMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.world_batch = None
		self.world_group = None

		self.world = None
		self.camera = None
		self.background = None

		self.total_time = 0
		self.current_planet = None
		self.poi_data = None

		self.container = None
		self.button_container = None

		self.title = None
		self.start_button = None
		self.level_select_button = None
		self.level_editor_button = None
		self.options_button = None
		self.quit_button = None

	def on_click(self, x, y):
		# self.button_container.explode(500, 1)
		world_pos = HitZonePoint(self.camera.screen_to_world(x, y))
		for planet in self.world.planets:
			if planet.collides_with(world_pos):
				self.track_new_planet(planet=planet)
				self.total_time = 0
				return

	def on_resize(self, width, height):
		self.camera.on_resize(width, height)
		self.camera.set_anchor((width//2)*0.7, (height//2)*1)
		self.background.on_resize(width, height)

	def load(self):

		self.batch = pyglet.graphics.Batch()
		self.world_batch = pyglet.graphics.Batch()
		self.world_group = pyglet.graphics.Group()

		with open('swingbye/levels/main_menu.json') as file:
			level = json.load(file)

		self.world = parse_level(level, self.world_batch, self.world_group)

		self.current_planet = self.world.planets[0]
		self.poi_data = {
			'most_velocity': None,
			'most_velocity_change': None,
			'most_density': None,
			'most_distance': None,
			'most_zoom': None,
			'most_picks': None,
			'least_zoom': None,
			'least_picks': None,
			'least_distance': None,
			# TODO: planets that will collide are a good poi
			'on_collision_course': None,
			'previous_planet': None,
			'previous_velocities': [0] * len(self.world.planets),
			'picks': dict([(planet, 0) for planet in self.world.planets])
		}

		self.camera = Camera(self.window, smooth_level=1)
		self.camera.set_parent(self.current_planet)
		self.camera.set_anchor((self.window.width//3), (self.window.height//2))
		self.camera.set_zoom(0.75)

		self.background = BackgroundObject(level['background_sprite'], self.camera, self.batch, self.world_group)

		# UI AND STUFF
		self.container = Board()
		self.button_container = Around()

		# TODO: better logo and placement
		# logo = pyglet.resource.image('assets/logo.png')
		self.title = Image('assets/logo.png')
		self.start_button = MainMenuButton('Start\ngame', callback=self.to_game, radius=75, background_sprite='assets/sprites/planet1.png')
		self.level_select_button = MainMenuButton('Select\nlevel', callback=self.to_level_select_menu, radius=75, background_sprite='assets/sprites/planet2.png')
		self.level_editor_button = MainMenuButton('Level\neditor', callback=self.to_level_editor, radius=75, background_sprite='assets/sprites/planet3.png')
		self.options_button = MainMenuButton('Options', callback=self.to_options_menu, radius=75, background_sprite='assets/sprites/planet4.png')
		self.quit_button = MainMenuButton('Quit\ngame', callback=exit, radius=75, background_sprite='assets/sprites/planet5.png')

		self.button_container.add(self.start_button, distance=250, angle=0)
		self.button_container.add(self.level_select_button, distance=275, angle=50)
		self.button_container.add(self.level_editor_button, distance=300, angle=90)
		self.button_container.add(self.options_button, distance=275, angle=130)
		self.button_container.add(self.quit_button, distance=250, angle=180)

		self.container.add(self.title, center_percent=(0.15, 0.9), width_percent=0.3, height_percent=0.2)
		self.container.add(self.button_container, bottom_left_percent=(0.5, 0), width_percent=0.5, height_percent=1)

	def to_game(self):
		self.window.transition_to_scene('Level')

	def to_level_select_menu(self):
		self.window.transition_to_scene('LevelSelectMenu')

	def to_level_editor(self):
		self.window.transition_to_scene('Editor')

	def to_options_menu(self):
		self.window.transition_to_scene('OptionsMenu')

	def begin(self):

		self.gui.clear()

		self.load()

		self.gui.add(self.container)

	def end(self):
		if self.world is not None:
			for planet in self.world.planets:
				planet.delete()
			self.background.delete()
			self.background = None
			self.world = None
			self.camera = None

	def draw(self):
		self.batch.draw()
		with self.camera:
			self.world_batch.draw()
		self.gui.batch.draw()

	def run(self, dt):
		self.camera.update(dt)
		self.total_time += dt
		if self.total_time > 10:
			self.total_time %= 10
			self.track_new_planet()

		self.world.step(5)

	def track_new_planet(self, planet=None):
		if planet is None:
			self.current_planet = self.get_poi()
		else:
			self.current_planet = planet
		self.camera.set_parent(self.current_planet)
		self.camera.set_anchor((self.window.width//3), (self.window.height//2))
		self.camera.target_zoom = self.get_zoom_at_distance(self.current_planet.pos.length())

	def get_zoom_at_distance(self, x):
		return -0.0000005 * x * (x - 2000) + 0.2

	def get_poi(self):
		most_velocity = 0
		most_velocity_change = 0
		most_density = np.inf
		most_distance = 0
		least_distance = np.inf
		most_picks = 0
		least_picks = np.inf
		most_zoom = 0
		least_zoom = np.inf
		for i, planet in enumerate(self.world.planets):
			vel = planet.vel
			pos = planet.pos
			current_velocity = vel.length()
			if current_velocity > most_velocity:
				most_velocity = current_velocity
				self.poi_data['most_velocity'] = planet

			current_velocity_change = abs(current_velocity - self.poi_data['previous_velocities'][i])
			if current_velocity_change > most_velocity_change:
				most_velocity_change = current_velocity_change
				self.poi_data['most_velocity_change'] = planet

			# Do not use the sun's distance... from the sun
			current_distance = pos.length() if (pos[0] != 0 and pos[1] != 0) else np.inf
			if current_distance > most_distance:
				most_distance = current_distance
				self.poi_data['most_distance'] = planet
			if current_distance < least_distance:
				least_distance = current_distance
				self.poi_data['least_distance'] = planet

			current_zoom = self.get_zoom_at_distance(current_distance)
			if current_zoom > most_zoom:
				most_zoom = current_zoom
				self.poi_data['most_zoom'] = planet
			if current_zoom < least_zoom:
				least_zoom = current_zoom
				self.poi_data['least_zoom'] = planet

			current_density = min(most_density, sum([(p.pos - pos).length() for p in self.world.planets if p is not planet]) / len(self.world.planets))
			if current_density < most_density:
				most_density = current_density
				self.poi_data['most_density'] = planet

			current_picks = self.poi_data['picks'][planet]
			if current_picks > most_picks:
				most_picks = current_picks
				self.poi_data['most_picks'] = planet
			if current_picks < least_picks:
				least_picks = current_picks
				self.poi_data['least_picks'] = planet

			self.poi_data['previous_velocities'][i] = current_velocity

		candidates = [
			# self.poi_data['most_velocity'],
			self.poi_data['most_velocity_change'],
			self.poi_data['most_density'],
			self.poi_data['most_distance'],
			self.poi_data['most_zoom'],
			self.poi_data['least_zoom'],
			self.poi_data['least_picks'],
			self.poi_data['least_distance']
		]
		# TODO: fix planets getting picked twice, despite this filter...
		wanted = lambda p: (p.radius > 5)
		# wanted = lambda p: ((p is self.poi_data['previous_planet']) or (p is self.poi_data['most_picks']) or (p.radius > 5))
		candidates = filter(wanted, candidates)

		picked = np.random.choice(list(candidates))

		self.poi_data['picks'][picked] += 1
		self.poi_data['previous_planet'] = picked

		# pprint(self.poi_data)

		# System is still improvable
		# After a few iterations, we get this result:
		# [70, 41, 22, 33, 25, 55, 23, 23]
		# The sun is getting picked a lot (which is good!), but one of saturn's moons too, which is meh
		# The comet isn't getting picked a lot either (last in list)
		# Otherwise, this was fun to try to figure out!

		return picked
