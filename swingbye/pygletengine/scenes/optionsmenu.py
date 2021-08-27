from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.components.buttons import Button, CycleButton
from swingbye.pygletengine.components.labels import Title
from swingbye.pygletengine.components.containers import VBox
from swingbye.pygletengine.globals import TITLE_SIZE_PROPORTION


class OptionsMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.container = VBox()

		self.title = Title('Options')
		self.option_1_button = Button('Option Button 1')
		self.option_2_button = Button('Option Button 2')
		self.option_1_cycle = CycleButton({'1': 'Option cycle 1', '2': 'Option cycle 2', '3': 'Option cycle 3'})
		self.option_2_cycle = CycleButton({'ON': 'Option ON', 'OFF': 'Option OFF'})
		self.back_button = Button('Back', self.to_main_menu)

		self.container.add(self.title, size=int(self.window.height*TITLE_SIZE_PROPORTION))
		self.container.add(self.option_1_button)
		self.container.add(self.option_2_button)
		self.container.add(self.option_1_cycle)
		self.container.add(self.option_2_cycle)
		self.container.add(self.back_button)

	def to_main_menu(self):
		self.window.transition_to_scene('MainMenu')

	def begin(self):
		self.gui.clear()
		self.load()
		self.gui.add(self.container)

	def draw(self):
		self.gui.batch.draw()
