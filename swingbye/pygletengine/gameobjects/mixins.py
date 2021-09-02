import pyglet
from typing import Optional
from swingbye.pygletengine.utils import create_sprite
from swingbye.pygletengine.components.paths import Path, LinePath

class SpriteMixin:
	"""SpriteMixin adds a sprite to a `physics.entity.ExplicitEntity` or `physics.entity.ImplicitEntity` class, and intercepts the position setter to update its own sprite position"""

	def __init__(self, sprite: pyglet.sprite.Sprite = create_sprite('assets/sprites/missingtexture.png')):
		self.sprite = sprite

	def _get_pos(self):
		return super().pos

	def _set_pos(self, pos):
		super()._set_pos(pos)
		self.sprite.position = (pos.x, pos.y)

	pos = property(_get_pos, _set_pos)


class PathMixin:
	# TODO : union LinePath and PointPath

	def __init__(self, path: LinePath = LinePath()):
		self.path = path

	def _get_prediction(self):
		return super().prediction

	def _set_prediction(self, prediction):
		super()._set_prediction(prediction)
		self.path.vertices = prediction

	prediction = property(_get_prediction, _set_prediction)
