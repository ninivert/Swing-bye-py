import glooey
import pyglet
import math
from .scene import Scene
from ..components.graph import Graph
from ..components.containers import VBox
from ..globals import WINDOW_WIDTH, WINDOW_HEIGHT


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
