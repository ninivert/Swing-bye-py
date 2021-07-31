import pyglet
import glooey
from numpy import interp, inf
from .containers import Frame
from ..gameobjects.linepath import LinePath


class Graph(glooey.Widget):
	custom_alignment = 'fill'

	def __init__(self, width, height, color=(255, 255, 255), y_scale_mode='auto', min_y=0, max_y=1, query=None, sample_size=100, sample_rate=1/10):
		super().__init__()
		
		self.frame = Frame()

		self.graph_width = width
		self.graph_height = height
		self.color = color

		self.y_scale_modes = {
			'auto': self._auto_y_scale,
			'smooth': self._smooth_y_scale,
			'fixed_min': self._fixed_min_y_scale,
			'fixed_max': self._fixed_max_y_scale,
			'fixed': lambda: None
		}
		self.y_scale_mode = y_scale_mode
		self.min_y = min_y
		self.max_y = max_y
		if self.y_scale_mode not in self.y_scale_modes:
			raise ValueError(f'y_scale_mode can only be {list(self.y_scale_modes.keys())} while you provided `{y_scale_mode}`')

		self.query = query
		self.sample_size = sample_size
		self.sample_rate = sample_rate
		self.samples = []

		self.graph = None

		self._attach_child(self.frame)

	def _get_min_max_y(self):
		min_y, max_y = +inf, -inf
		for sample in self.samples:
			min_y = min(min_y, sample)
			max_y = max(max_y, sample)
		return min_y, max_y

	def _auto_y_scale(self):
		min_y, max_y = self._get_min_max_y()
		self.min_y = min(min_y, self.min_y)
		self.max_y = max(max_y, self.max_y)

	def _smooth_y_scale(self):
		min_y, max_y = self._get_min_max_y()
		lerp = lambda a, b, c: a + c*(b - a)
		self.min_y = lerp(self.min_y, min_y, 0.1)
		self.max_y = lerp(self.max_y, max_y, 0.1)

	def _fixed_min_y_scale(self):
		min_y, max_y = self._get_min_max_y()
		self.max_y = max_y

	def _fixed_max_y_scale(self):
		min_y, max_y = self._get_min_max_y()
		self.min_y = min_y

	def _calulate_point_positions(self):
		self.x, self.y = self.rect.bottom_left
		vertices = []
		for i in range(len(self.samples)):
			x = self.x + (self.graph_width * (i / len(self.samples)))
			y = self.y + float(interp(self.samples[i], [self.min_y, self.max_y], [0, self.graph_height]))
			vertices.append((int(x), int(y)))  # casting to ints for safety
		return vertices

	def load(self):
		self.graph = LinePath(
			self.batch,
			point_count=self.sample_size,
			points=self._calulate_point_positions(),
			color=self.color
		)
		if self.query is not None:
			pyglet.clock.schedule_interval(self.update_data, self.sample_rate)

	def update_data(self, dt):
		if len(self.samples) >= self.sample_size:
			self.samples.pop(0)

		self.samples.append(self.query())

		self.y_scale_modes[self.y_scale_mode]()

		if self.graph is not None:
			self.graph.vertices = self._calulate_point_positions()

	def reset(self):
		self.samples.clear()

	def do_claim(self):
		return self.graph_width, self.graph_height

	def do_draw(self):
		if self.graph is None:
			self.load()

	def do_undraw(self):
		if self.graph is not None:
			self.graph.delete()
			self.graph = None

