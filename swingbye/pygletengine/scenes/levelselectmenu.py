import glooey
from .scene import Scene
from ..components.buttons import Button
from ..components.labels import Title
from ..components.containers import VBox, Grid
from ..globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION


class LevelSelectMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.container = VBox()

		level_grid = Grid()

		for i in range(2):
			for j in range(3):
				level_grid.add(i, j, Button(f'Level {(i+1)*(j+1)}'))

		self.container.add(Title('Level Select'), size=int(WINDOW_HEIGHT*TITLE_SIZE_PROPORTION))
		self.container.add(level_grid)
		self.container.add(Button('Back', action=self.callback, action_params=['MainMenu']), size=0)

	def begin(self):
		
		self.gui.clear()

		self.load()

		self.gui.add(self.container)

	def draw(self):
		self.gui.batch.draw()
