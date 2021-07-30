import glooey
from pyglet.app import exit
from .scene import Scene
from ..components.buttons import Button
from ..components.labels import Title
from ..components.containers import VBox
from ..globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION


class MainMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.container = VBox()

		self.container.add(Title('Swing BYE'), size=int(WINDOW_HEIGHT*TITLE_SIZE_PROPORTION))
		self.container.add(Button('Start game', action=self.callback, action_params=['Level']))
		self.container.add(Button('Select level', action=self.callback, action_params=['LevelSelectMenu']))
		self.container.add(Button('Options', action=self.callback, action_params=['OptionsMenu']))
		self.container.add(Button('Quit game', action=exit))

	def begin(self):
		
		self.gui.clear()

		self.load()

		self.gui.add(self.container)
	
	def draw(self):
		self.gui.batch.draw()
