import glooey
import pyglet
from .scene import Scene
from ..components.buttons import Button, CycleButton
from ..components.labels import Title
from ..components.containers import VBox
from ..globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION


class OptionsMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.container = VBox()

		self.container.add(Title('Options'), size=int(WINDOW_HEIGHT*TITLE_SIZE_PROPORTION))
		self.container.add(Button('Option Button 1'))
		self.container.add(Button('Option Button 2'))
		self.container.add(CycleButton({'1': 'Option cycle 1', '2': 'Option cycle 2', '3': 'Option cycle 3'}))
		self.container.add(CycleButton({'ON': 'Option ON', 'OFF': 'Option OFF'}))
		self.container.add(Button('Back', action=self.callback, action_params=['MainMenu']), size=0)

	def begin(self):
		
		self.gui.clear()

		self.load()

		self.gui.add(self.container)

	def draw(self):
		self.gui.batch.draw()
