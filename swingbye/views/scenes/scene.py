import abc


class Scene(abc.ABC):

	def __init__(self, ctx, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ctx = ctx

	@abc.abstractmethod
	def begin(self):
		raise NotImplementedError()

	@abc.abstractmethod
	def load(self):
		raise NotImplementedError()