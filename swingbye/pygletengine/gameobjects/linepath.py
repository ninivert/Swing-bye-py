import pyglet


class LinePath:
	def __init__(self, point_count=0, points=[], color=(255, 255, 255), batch=None, group=None):
		if point_count > len(points):
			raise ValueError(f'Provided {point_count=} is less than length of vertices={len(points)}')

		# Extend points to match point_count
		if len(points) < point_count:
			for i in range(len(points) - point_count):
				points.append((0, 0))

		self._vertex_length = point_count + 2

		self._load_vertices_from_tuples(points)
		self._generate_vertex_color_list(color)

		if batch is not None:
			self.batch = batch
		if group is not None:
			self.group = group

		self.vertex_list = self.batch.add(
			self.vertex_length,
			pyglet.gl.GL_LINE_STRIP,
			self.group,
			('v2i/stream', self.vertices),
			('c3B/dynamic', self.color)
		)

	def _load_vertices_from_tuples(self, tuple_list):
		self._vertices = [*tuple_list[0]]
		for vert in tuple_list:
			self._vertices.extend(vert)
		self._vertices.extend(*tuple_list[-1])

	def _generate_vertex_color_list(self, color):
		self._color = []
		for i in range(self._vertex_length):
			self._color.extend(color)

	@property
	def vertices(self):
		return self._vertices

	@vertices.setter
	def vertices(self, points):
		self._load_vertices_from_tuples(points)
		self.vertex_list.vertices = self._vertices

	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, color):
		self._generate_vertex_color_list(color)
		self.vertex_list.colors = self._color

	@property
	def vertex_length(self):
		# Actual point count (removing duplicates at beginning and end)
		return self._vertex_length - 2

	@vertex_length.setter
	def vertex_length(self, length):
		# Not sure if this works without also modifying the vertices
		self.vertex_list.resize(length + 2)
		self._vertex_length = length + 2
