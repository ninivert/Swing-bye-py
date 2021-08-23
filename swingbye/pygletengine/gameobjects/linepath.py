import pyglet
from typing import Union

class LinePath:
	def __init__(self, point_count=1, points=[], color=(255, 255, 255), batch=None, group=None):
		if len(points) > point_count:
			raise ValueError(f'Provided {point_count=} is less than length of vertices={len(points)}')

		self._vertex_length = point_count + 2

		# Extend points to match point_count
		points = self._complete_vertices_with_empty(points)

		self._load_vertices_from_tuples(points)
		self._generate_vertex_color_list(color)

		# Default empty vertex list
		self.vertex_list = pyglet.graphics.vertex_list(
			self._vertex_length,
			('v2f/stream', self._vertices),
			('c3B/dynamic', self._color)
		)

		if group is None:
			self.group = pyglet.graphics.Group()
		else:
			self.group = group
		self.batch = batch

	@property
	def batch(self):
		return self._batch

	@batch.setter
	def batch(self, batch: Union[None, pyglet.graphics.Batch]):
		self._batch = batch

		if batch is not None:
			self.vertex_list = self.batch.add(
				self._vertex_length,
				pyglet.gl.GL_LINE_STRIP,
				self.group,
				('v2f/stream', self._vertices),
				('c3B/dynamic', self._color)
			)

	def _complete_vertices_with_empty(self, points):
		if len(points) < self._vertex_length - 2:
			for i in range(self._vertex_length - 2 - len(points)):
				points.append((0, 0))
		return points

	def _complete_vertices_with_duplicates(self, points):
		if len(points) < self._vertex_length - 2:
			last_point = points[-1]
			for i in range(self._vertex_length - 2 - len(points)):
				points.append(last_point)
		return points

	def _load_vertices_from_tuples(self, tuple_list):
		self._vertices = [*tuple_list[0]]
		for vert in tuple_list:
			self._vertices.extend(vert)
		self._vertices.extend(tuple_list[-1])

	def _generate_vertex_color_list(self, color):
		self._color = []
		for i in range(self._vertex_length):
			self._color.extend(color)

	def delete(self):
		self.vertex_list.delete()

	@property
	def vertices(self):
		return self._vertices

	@vertices.setter
	def vertices(self, points):
		self._complete_vertices_with_duplicates(points)
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
