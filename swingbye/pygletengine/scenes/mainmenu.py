import pyglet
import json
from pyglet.app import exit
from swingbye.levels.parser import parse_level
from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.scenes.layers.camera import Camera
from swingbye.pygletengine.components.buttons import Button
from swingbye.pygletengine.components.labels import Title
from swingbye.pygletengine.components.containers import Freeform
from swingbye.pygletengine.globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION


class MainMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):

		# BACKGROUND
		self.world_batch = pyglet.graphics.Batch()
		self.world_group = pyglet.graphics.Group()

		with open('swingbye/levels/main_menu.json') as file:
			level = json.load(file)

		self.world = parse_level(level, self.world_batch, self.world_group)
		self.camera = Camera(self.window)
		self.camera.set_position(-self.window.width//2, -self.window.height//2)

		# UI AND STUFF
		self.container = Freeform()

		self.title = Title('Swing BYE')
		self.start_button = Button('Start game', self.to_game)
		self.level_select_button = Button('Select level', self.to_level_select_menu)
		self.options_button = Button('Options', self.to_options_menu)
		self.quit_button = Button('Quit game', exit)

		self.container.add(self.title, x=0.1, y=0.8, width=420, height=100)
		self.container.add(self.start_button, x=0.7, y=0.7, width=250, height=50)
		self.container.add(self.level_select_button, x=0.7, y=0.6, width=250, height=50)
		self.container.add(self.options_button, x=0.7, y=0.5, width=250, height=50)
		self.container.add(self.quit_button, x=0.7, y=0.4, width=250, height=50)

	def to_game(self):
		self.window.transition_to_scene('Level')

	def to_level_select_menu(self):
		self.window.transition_to_scene('LevelSelectMenu')

	def to_options_menu(self):
		self.window.transition_to_scene('OptionsMenu')

	def begin(self):
		
		self.gui.clear()

		self.load()

		self.gui.add(self.container)
	
	def draw(self):
		with self.camera:
			self.world_batch.draw()
		self.gui.batch.draw()
