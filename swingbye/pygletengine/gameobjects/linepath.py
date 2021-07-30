import pyglet


class LinePath:
	def __init__(self, batch, point_count=1, points=[], color=(255, 255, 255), group=None):
		if len(points) > point_count:
			raise ValueError(f'Provided {point_count=} is less than length of vertices={len(points)}')

		# Extend points to match point_count
		if len(points) < point_count:
			for i in range(point_count - len(points)):
				points.append((0, 0))

		self._vertex_length = point_count + 2

		self._load_vertices_from_tuples(points)
		self._generate_vertex_color_list(color)

		self.batch = batch
		self.group = group

		self.vertex_list = self.batch.add(
			self._vertex_length,
			pyglet.gl.GL_LINE_STRIP,
			self.group,
			('v2i/stream', self._vertices),
			('c3B/dynamic', self._color)
		)

	def _load_vertices_from_tuples(self, tuple_list):
		self._vertices = [*tuple_list[0]]
		for vert in tuple_list:
			self._vertices.extend(vert)
		self._vertices.extend(tuple_list[-1])

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


if __name__ == '__main__':
	win = pyglet.window.Window()
	batch = pyglet.graphics.Batch()
	lp1 = LinePath(batch)
	@win.event
	def on_draw(): batch.draw()
	pyglet.app.run()
