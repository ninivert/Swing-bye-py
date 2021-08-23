import glooey
from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.components.buttons import Button
from swingbye.pygletengine.components.labels import Title
from swingbye.pygletengine.components.containers import VBox, Grid
from swingbye.pygletengine.globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION


class LevelSelectMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.container = VBox()

		self.button_grid = Grid()

		for i in range(2):
			for j in range(3):
				self.button_grid.add(i, j, Button(f'Level {(i+1)*(j+1)}'))

		self.title = Title('Level Select')
		self.back_button = Button('Back')

		self.back_button.set_handler('on_press', self.to_main_menu)

		self.container.add(self.title, size=int(WINDOW_HEIGHT*TITLE_SIZE_PROPORTION))
		self.container.add(self.button_grid)
		self.container.pack(self.back_button)

	def to_main_menu(self):
		self.window.transition_to_scene('MainMenu')

	def begin(self):
		
		self.gui.clear()

		self.load()

		self.gui.add(self.container)

	def draw(self):
		self.gui.batch.draw()
