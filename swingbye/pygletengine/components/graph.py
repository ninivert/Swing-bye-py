import pyglet
import glooey
from numpy import interp, inf
from ..gameobjects.linepath import LinePath


class Graph(glooey.Widget):
	custom_alignment = 'fill'

	def __init__(self, width, height, color=(255, 255, 255), y_scale_mode='auto', min_y=0, max_y=1, query=None, sample_size=100, sample_rate=1/10):
		super().__init__()

		# Graph options
		self.graph_width = width
		self.graph_height = height
		self.color = color

		# Graph scaling options
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

		# Graph data
		self._query = query
		self._sample_size = sample_size
		self._sample_rate = sample_rate
		self.samples = []

		self.graph = None

		self.label_font_size = 10
		self.max_label = None
		self.min_label = None

		self.loaded = False

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

	@property
	def sample_rate(self):
		return self._sample_rate

	@sample_rate.setter
	def sample_rate(self, sample_rate):
		self._sample_rate = sample_rate
		pyglet.clock.unschedule(self.update_data)
		pyglet.clock.schedule_interval(self.update_data, self._sample_rate)

	@property
	def sample_size(self):
		return self._sample_size

	@sample_size.setter
	def sample_size(self, sample_size):
		self._sample_size = sample_size
		self.graph.vertex_length = self._sample_size

	@property
	def query(self):
		return self._query

	@query.setter
	def query(self, query):
		self._query = query
		if self._query is None:
			pyglet.clock.unschedule(self.update_data)
		else:
			pyglet.clock.unschedule(self.update_data)
			pyglet.clock.schedule_interval(self.update_data, self._sample_rate)

	def load(self):
		x, y = self.get_rect().bottom_left
		self.graph = LinePath(
			self.batch,
			point_count=self._sample_size,
			points=self._calulate_point_positions(),
			color=self.color,
			group=self.group
		)
		self.max_label = pyglet.text.Label(
			font_size=self.label_font_size,
			x=x, y=y+self.graph_height,
			anchor_x='left', anchor_y='top',
			batch=self.batch,
			group=self.group
		)
		self.min_label = pyglet.text.Label(
			font_size=self.label_font_size,
			x=x, y=y,
			anchor_x='left', anchor_y='bottom',
			batch=self.batch,
			group=self.group
		)
		self.resume_sampling()
		self.loaded = True

	def update_labels(self):
		self.max_label.text = f'{self.max_y:.1f}'
		self.min_label.text = f'{self.min_y:.1f}'

	def update_data(self, dt):
		if self.loaded:
			if len(self.samples) >= self._sample_size:
				self.samples.pop(0)

			self.samples.append(self._query())

			self.y_scale_modes[self.y_scale_mode]()

			self.update_labels()

			self.graph.vertices = self._calulate_point_positions()

	def reset(self):
		self.samples.clear()

	def pause_sampling(self):
		if self._query is not None:
			pyglet.clock.unschedule(self.update_data)

	def resume_sampling(self):
		if self._query is not None:
			pyglet.clock.schedule_interval(self.update_data, self._sample_rate)

	def do_claim(self):
		return self.graph_width + sum(self.horz_padding), self.graph_height + sum(self.vert_padding)

	def do_draw(self):
		if not self.loaded:
			self.load()

	def do_undraw(self):
		if self.loaded:
			self.graph.delete()
			self.graph = None
			self.max_label.delete()
			self.max_label = None
			self.min_label.delete()
			self.min_label = None
			self.loaded = False
			self.pause_sampling()
