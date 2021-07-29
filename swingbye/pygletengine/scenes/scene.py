import abc


class Scene(abc.ABC):

	def __init__(self, gui, callback, event_manager, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.gui = gui
		self.callback = callback
		self.event_manager = event_manager

	@abc.abstractmethod
	def begin(self):
		raise NotImplementedError()

	@abc.abstractmethod
	def load(self):
		raise NotImplementedError()

	@abc.abstractmethod
	def draw(self):
		raise NotImplementedError()

	def run(self, dt):
		pass
