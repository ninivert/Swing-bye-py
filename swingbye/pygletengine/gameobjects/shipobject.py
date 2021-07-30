from ...physics.ship import Ship
from .utils import SpriteMixin
from dataclasses import dataclass

@dataclass
class ShipObject(SpriteMixin, Ship):
	def __post_init__(self):
		scale = 0.05  # self.r / (self.sprite.width//2)
		self.sprite.update(x=self.pos[0], y=self.pos[1], scale=scale)
