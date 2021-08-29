import pyglet
import json
import numpy as np
from pyglet.app import exit
from swingbye.levels.parser import parse_level
from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.scenes.layers.camera import Camera
from swingbye.pygletengine.components.buttons import Button
from swingbye.pygletengine.components.labels import Title
from swingbye.pygletengine.components.containers import Freeform
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

		self.title = None
		self.start_button = None
		self.level_select_button = None
		self.level_editor_button = None
		self.options_button = None
		self.quit_button = None

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

		self.camera = Camera(self.window, smooth_level=0.01)
		self.camera.set_parent(self.current_planet)
		self.camera.set_anchor((self.window.width//2)*0.3, (self.window.height//2)*0.3)
		self.camera.set_zoom(0.5)

		self.background = BackgroundObject(level['background_sprite'], self.camera, self.batch, self.world_group)

		# UI AND STUFF
		self.container = Freeform()

		self.title = Title('Swing BYE')
		self.start_button = Button('Start game', self.to_game)
		self.level_select_button = Button('Select level', self.to_level_select_menu)
		self.level_editor_button = Button('Level editor', self.to_level_editor)
		self.options_button = Button('Options', self.to_options_menu)
		self.quit_button = Button('Quit game', exit)

		self.container.add(self.title, x=0.1, y=0.8, width=420, height=100)
		self.container.add(self.start_button, x=0.7, y=0.7, width=250, height=50)
		self.container.add(self.level_select_button, x=0.7, y=0.6, width=250, height=50)
		self.container.add(self.level_editor_button, x=0.7, y=0.5, width=250, height=50)
		self.container.add(self.options_button, x=0.7, y=0.4, width=250, height=50)
		self.container.add(self.quit_button, x=0.7, y=0.3, width=250, height=50)

	def to_game(self):
		self.window.transition_to_scene('Level')

	def to_level_select_menu(self):
		self.window.transition_to_scene('LevelSelectMenu')

	def to_level_editor(self):
		self.window.transition_to_scene('Editor')

	def to_options_menu(self):
		self.window.transition_to_scene('OptionsMenu')

	def on_resize(self, width, height):
		self.camera.on_resize(width, height)
		self.camera.set_anchor((width//2)*0.7, (height//2)*1)
		self.background.on_resize(width, height)

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
		self.total_time += dt
		if self.total_time > 10:
			self.total_time %= 10
			self.current_planet = self.get_poi()
			self.camera.set_parent(self.current_planet)
			self.camera.set_anchor((self.window.width//2)*0.7, (self.window.height//2)*1)
			self.camera.target_zoom = self.get_zoom_at_distance(np.linalg.norm(self.current_planet.pos))

		# TODO: find out why world.step breaks everything in other scenes...
		self.world.time += 5
	
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
			current_velocity = np.linalg.norm(vel)
			if current_velocity > most_velocity:
				most_velocity = current_velocity
				self.poi_data['most_velocity'] = planet

			current_velocity_change = abs(current_velocity - self.poi_data['previous_velocities'][i])
			if current_velocity_change > most_velocity_change:
				most_velocity_change = current_velocity_change
				self.poi_data['most_velocity_change'] = planet
			
			current_distance = np.linalg.norm(pos)
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
			
			current_density = min(most_density, sum([np.linalg.norm(p.pos - pos) for p in self.world.planets if p is not planet]) / len(self.world.planets))
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
		candidates = list(filter(lambda p: p is not self.poi_data['previous_planet'] or p is not self.poi_data['most_picks'], candidates))
		
		picked = np.random.choice(candidates)

		self.poi_data['picks'][picked] += 1
		self.poi_data['previous_planet'] = picked

		# System is still improvable
		# After a few iterations, we get this result:
		# [70, 41, 22, 33, 25, 55, 23, 23]
		# The sun is getting picked a lot (which is good!), but one of saturn's moons too, which is meh
		# The comet isn't getting picked a lot either (last in list)
		# Otherwise, this was fun to try to figure out!

		return picked

