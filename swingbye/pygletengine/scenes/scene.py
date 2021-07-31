import pyglet


class Scene:

	def __init__(self, gui, callback, *args, **kwargs):
		super().__init__()
		self.gui = gui
		self.callback = callback

	def begin(self):
		raise NotImplementedError('abstract')

	def load(self):
		raise NotImplementedError('abstract')

	def draw(self):
		raise NotImplementedError('abstract')

	def run(self, dt):
		pass
