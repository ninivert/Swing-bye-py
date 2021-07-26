import numpy as np
import logging
from typing import List
from .entity import ImplicitEntity
from .ship import Ship
from .planet import Planet
from .globals import GRAVITY_CST, GRAVITY_SINGULARITY_OFFSET
from .integrator import Integrator

_logger = logging.getLogger(__name__)

class World():
	def __init__(
		self,
		ship: Ship,
		planets: List[Planet],
		integrator: Integrator
	):
		self.planets = planets
		self.ship = ship
		self.integrator = integrator
		self.t = 0

	def get_forces_on(self, titty: ImplicitEntity, t: float = None):
		if t is None:
			t = self.t

		f = np.zeros(2)
		for planet in self.planets:
			r = planet.get_pos(t) - titty.x
			d = np.linalg.norm(r)
			n = r/d
			f += GRAVITY_CST*(titty.m + planet.m)/(d+GRAVITY_SINGULARITY_OFFSET)**2 * n

		return f

	def step(self, dt: float):
		if not self.ship.docked:
			self.integrator(self.ship, self.get_forces_on, self.t, dt)

	def set_time(self, t: float):
		if not self.ship.docked:
			_logger.warning('changing world time but ship is not docked to a planet !')

	def __str__(self):
		res = super().__str__()
		res += '\n\t' + self.ship.__str__()
		res += '\nPlanets'
		for planet in self.planets:
			res += '\n\t' + planet.__str__()
		return res


if __name__ == '__main__':
	from .integrator import EulerIntegrator

	world = World(
		Ship(np.array([100.0, 100.0])),
		[Planet(s=50)],
		EulerIntegrator()
	)

	print(world)

	world.step(0.1)
	world.step(0.1)

	print(world)
