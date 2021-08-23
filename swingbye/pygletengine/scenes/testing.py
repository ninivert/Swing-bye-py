import pyglet
import math
from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.components.graph import Graph
from swingbye.pygletengine.components.containers import VBox
from swingbye.pygletengine.globals import WINDOW_WIDTH, WINDOW_HEIGHT


# Testing environment for testing new custom widgets and stuff


class Test(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.container = VBox()

		self.container.add(
			Graph(
				WINDOW_WIDTH, WINDOW_HEIGHT,
				query=lambda x: math.sin(x)*100
			)
		)

	def begin(self):
		
		self.gui.clear()

		self.load()

		self.gui.add(self.container)
	
	def draw(self):
		self.gui.batch.draw()
