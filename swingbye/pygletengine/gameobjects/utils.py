from ..utils import create_sprite
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
