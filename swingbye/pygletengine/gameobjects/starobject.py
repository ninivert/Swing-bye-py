from random import random
from ...physics.entity import ImplicitEntity
from .utils import SpriteMixin
from dataclasses import dataclass


@dataclass
class StarObject(SpriteMixin, ImplicitEntity):
	def __post_init__(self):
		scale = 1 + random()
		self.sprite.update(x=self.pos[0], y=self.pos[1], scale=scale)
