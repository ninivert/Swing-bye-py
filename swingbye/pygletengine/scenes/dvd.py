import pyglet
from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.gameobjects.dvdobject import DVDobject
from swingbye.pygletengine.globals import WINDOW_WIDTH, WINDOW_HEIGHT


class DVD(Scene):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.batch = pyglet.graphics.Batch()
		self.dvd = DVDobject(
			'assets/dvd.png',
			0, 0,
			200, 80,
			[
				(255, 20, 20),
				(20, 255, 20),
				(20, 20, 255),
				(255, 255, 20),
				(255, 20, 255)
			],
			WINDOW_WIDTH, WINDOW_HEIGHT,
			batch=self.batch
		)

	def begin(self):
		self.gui.clear()

		self.load()

	def draw(self):
		self.batch.draw()

	def run(self, dt):
		self.dvd.update(dt)
