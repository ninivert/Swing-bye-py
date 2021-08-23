from ..utils import create_sprite
from .pointpath import PointPath
from dataclasses import dataclass
import pyglet

@dataclass
class SpriteMixin:
	"""SpriteMixin adds a sprite to a `physics.entity.ExplicitEntity` or `physics.entity.ImplicitEntity` class, and intercepts the position setter to update its own sprite position"""

	sprite: pyglet.sprite.Sprite = create_sprite('assets/sprites/missingtexture.png')
	# name: str = ''

	def _get_pos(self):
		return super().pos

	def _set_pos(self, pos):
		super()._set_pos(pos)
		if type(pos) is not property:
			self.sprite.position = (pos[0], pos[1])

	pos = property(_get_pos, _set_pos)


@dataclass
class PredictionMixin:
	# TODO : union LinePath
	path: PointPath = PointPath()

	def _get_prediction(self):
		return super().prediction

	def _set_prediction(self, prediction):
		super()._set_prediction(prediction)
		if type(prediction) is not property:
			self.path.vertices = prediction

	prediction = property(_get_prediction, _set_prediction)
