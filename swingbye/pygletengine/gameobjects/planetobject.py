from swingbye.physics.planet import Planet
from swingbye.pygletengine.gameobjects.utils import SpriteMixin, PredictionMixin
from dataclasses import dataclass


@dataclass
class PlanetObject(SpriteMixin, PredictionMixin, Planet):
	def __post_init__(self):
		scale = self.radius / (self.sprite.width//2)
		self.sprite.update(x=self.pos[0], y=self.pos[1], scale=scale)
