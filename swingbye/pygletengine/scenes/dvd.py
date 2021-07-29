import pyglet
from .scene import Scene
from ..gameobjects.dvdobject import DVDobject
from ..globals import WINDOW_WIDTH, WINDOW_HEIGHT


class DVD(Scene):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.bacth = pyglet.graphics.Batch()
		self.dvd = DVDobject(0, 0, 100, 40, [
			(255, 20, 20),
			(20, 255, 20),
			(20, 20, 255),
			(255, 255, 20),
			(255, 20, 255)],
			batch=self.batch
		)

	def begin(self):
		self.gui.clear()

		self.load()

	def draw(self):
		self.batch.draw()

	def run(self, dt):
		self.dvd.update(dt)
