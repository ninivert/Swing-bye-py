import pyglet
import glooey
from swingbye.pygletengine.components.paths import LinePath
from swingbye.pygletengine.utils import lerp
from numpy import interp, inf


class LineTHICKENER(pyglet.graphics.OrderedGroup):

	def __init__(self, order, thickness, parent=None):
		super().__init__(order, parent=parent)
		self.thickness = thickness

	def set_state(self):
		pyglet.gl.glLineWidth(self.thickness)

	def unset_state(self):
		pyglet.gl.glLineWidth(1)


class LineGraph(glooey.Widget):
	custom_alignment = 'fill'

	def __init__(self, width, height, lines=[], y_scale_mode='auto', min_y=0, max_y=0, sample_rate=1/10):
		super().__init__()

		# Graph options
		self.graph_width = width
		self.graph_height = height

		# Set default line options
		# TODO: validate lines?
		self.lines = lines
		if len(lines) == 0:
			self.lines.append(
				{
					'name': 'default',
					'path': None,
					'query': None,
					'color': (255, 255, 255, 255),
					'samples': [],
					'size': 100,
				}
			)

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

		self._sample_rate = sample_rate

		self.label_font_size = 10
		self.max_label = None
		self.min_label = None

		self.loaded = False

	def _get_min_max_y(self):
		min_y, max_y = +inf, -inf
		for line in self.lines:
			for sample in line['samples']:
				min_y = min(min_y, sample)
				max_y = max(max_y, sample)
		return min_y, max_y

	def _auto_y_scale(self):
		min_y, max_y = self._get_min_max_y()
		self.min_y = min(min_y, self.min_y)
		self.max_y = max(max_y, self.max_y)

	def _smooth_y_scale(self):
		min_y, max_y = self._get_min_max_y()
		self.min_y = lerp(self.min_y, min_y, 0.1)
		self.max_y = lerp(self.max_y, max_y, 0.1)

	def _fixed_min_y_scale(self):
		min_y, max_y = self._get_min_max_y()
		self.max_y = max_y

	def _fixed_max_y_scale(self):
		min_y, max_y = self._get_min_max_y()
		self.min_y = min_y

	def _calulate_point_positions(self, line):
		x, y = self.rect.bottom_left
		# TODO: use np
		vertices = []
		for i, val in enumerate(line['samples']):
			vert_x = x + (self.graph_width * (i / len(line['samples'])))
			vert_y = y + float(interp(val, [self.min_y, self.max_y], [0, self.graph_height]))
			vertices.append((int(vert_x), int(vert_y)))  # casting to ints for safety
		return vertices

	@property
	def sample_rate(self):
		return self._sample_rate

	@sample_rate.setter
	def sample_rate(self, sample_rate):
		self._sample_rate = sample_rate
		pyglet.clock.unschedule(self.update_data)
		pyglet.clock.schedule_interval(self.update_data, self._sample_rate)

	def get_sample_size(self, name):
		for line in self.lines:
			if line['name'] == name:
				return line['size']
		raise ValueError(f'Line {name} is not known')

	def set_sample_size(self, name, size):
		for line in self.lines:
			if line['name'] == name:
				line['size'] = size
				line['path'].vertex_length = size
				return

	def get_query(self, name):
		for line in self.lines:
			if line['name'] == name:
				return line['query']
		raise ValueError(f'Line {name} is not known')

	def set_query(self, name, query):
		for line in self.lines:
			if line['name'] == name:
				line['query'] = query

	def load(self):
		x, y = self.get_rect().bottom_left
		for i, line in enumerate(self.lines):
			line['path'] = LinePath(
				point_count=line['size'],
				points=self._calulate_point_positions(line),
				color=line['color'],
				batch=self.batch,
				group=LineTHICKENER(i, 3, parent=self.group)
			)
		self.max_label = pyglet.text.Label(
			font_size=self.label_font_size,
			x=x, y=y+self.graph_height,
			anchor_x='left', anchor_y='top',
			batch=self.batch,
			group=pyglet.graphics.OrderedGroup(1, parent=self.group)
		)
		self.min_label = pyglet.text.Label(
			font_size=self.label_font_size,
			x=x, y=y,
			anchor_x='left', anchor_y='bottom',
			batch=self.batch,
			group=pyglet.graphics.OrderedGroup(1, parent=self.group)
		)
		self.loaded = True
		self.resume_sampling()

	def update_labels(self):
		self.max_label.text = f'{self.max_y:.1f}'
		self.min_label.text = f'{self.min_y:.1f}'

	def update_data(self, dt):
		if self.loaded:
			# First, get the data
			for line in self.lines:
				if line['query'] is not None:
					if len(line['samples']) >= line['size']:
						line['samples'].pop(0)

					line['samples'].append(line['query']())

			# Secondly, set the correct scaling with the new data
			self.y_scale_modes[self.y_scale_mode]()
			self.update_labels()

			# Thirdly, update the vertex positions
			for line in self.lines:
					line['path'].vertices = self._calulate_point_positions(line)

	def reset(self):
		for line in self.lines:
			line['samples'].clear()

	def pause_sampling(self):
		pyglet.clock.unschedule(self.update_data)
		self.paused = True

	def resume_sampling(self):
		pyglet.clock.unschedule(self.update_data)
		pyglet.clock.schedule_interval(self.update_data, self._sample_rate)

	def do_claim(self):
		return self.graph_width + sum(self.horz_padding), self.graph_height + sum(self.vert_padding)

	def do_draw(self):
		if not self.loaded:
			self.load()

	def do_undraw(self):
		if self.loaded:
			for line in self.lines:
				line['path'].delete()
				line['path'] = None
			self.max_label.delete()
			self.max_label = None
			self.min_label.delete()
			self.min_label = None
			self.loaded = False
			self.pause_sampling()
