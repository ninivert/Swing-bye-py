import pyglet


class Scene(pyglet.event.EventDispatcher):

	def __init__(self, window, gui, callback, *args, **kwargs):
		super().__init__()
		self.window = window
		self.gui = gui
		# TODO: verify that this is safe to delete
		# self.callback = callback

	def begin(self):
		raise NotImplementedError('abstract')

	def load(self):
		raise NotImplementedError('abstract')

	def draw(self):
		raise NotImplementedError('abstract')

	def run(self, dt):
		pass
