import glooey
from pyglet.app import exit
from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.components.buttons import Button
from swingbye.pygletengine.components.labels import Title
from swingbye.pygletengine.components.containers import VBox
from ..globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION


class MainMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.container = VBox()

		self.title = Title('Swing BYE')
		self.start_button = Button('Start game')
		self.level_select_button = Button('Select level')
		self.options_button = Button('Options')
		self.quit_button = Button('Quit game')

		self.start_button.set_handler('on_press', self.to_game)
		self.level_select_button.set_handler('on_press', self.to_level_select_menu)
		self.options_button.set_handler('on_press', self.to_options_menu)
		self.quit_button.set_handler('on_press', exit)

		self.container.add(self.title, size=int(self.window.height*TITLE_SIZE_PROPORTION))
		self.container.add(self.start_button)
		self.container.add(self.level_select_button)
		self.container.add(self.options_button)
		self.container.add(self.quit_button)

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
		self.gui.batch.draw()
