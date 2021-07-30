from ...physics.planet import Planet
from .utils import SpriteMixin
from dataclasses import dataclass

@dataclass
class PlanetObject(SpriteMixin, Planet):
	def __post_init__(self):
		scale = self.radius / (self.sprite.width//2)
		self.sprite.update(x=self.pos[0], y=self.pos[1], scale=scale)
