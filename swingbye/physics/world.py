import numpy as np
import logging
from typing import List
from .entity import ImplicitEntity
from .ship import Ship
from .planet import Planet
from .globals import GRAVITY_CST, GRAVITY_SINGULARITY_OFFSET
from ..globals import SHIP_LAUNCH_SPEED, SHIP_PREDICTION_N, SHIP_PREDICTION_DT
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
		self._t = 0

	# Physics

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

		self.t += dt

	# Time handling

	@property
	def t(self, t: float):
		if not self.ship.docked:
			_logger.warning('changing world time but ship is not docked to a planet !')

		return self._t

	@t.setter()
	def t(self, t: float):
		self._t = t
		self.update_planets_location()

	# Game logic

	def launch_ship(self):
		self.ship.launch()

	def point_ship(self, n: np.ndarray):
		self.ship.pointing = n

	def update_ship_prediction(self):
		if not self.ship.docked:
			_logger.warning('ship prediction doesn\'t need to be updated since ship is launched')

		# HACK : not using deepcopy as that would be too slow
		temp_ship = Ship()
		temp_ship.x = self.ship.x
		temp_ship.m = self.ship.m
		temp_ship.parent = self.ship.parent
		temp_ship.pointing = self.ship.pointing
		temp_ship.launch()

		predictions = np.zeros((SHIP_PREDICTION_N, 2))

		for i, t in enumerate(np.linspace(self.t, self.t + SHIP_PREDICTION_N*SHIP_PREDICTION_DT, SHIP_PREDICTION_N)):
			self.integrator(temp_ship, self.get_forces_on, t, SHIP_PREDICTION_DT)
			predictions[i, :] = temp_ship.x

		self.ship.predictions = predictions

	def update_planets_location(self):
		for planet in self.planets:
			planet.x = planet.get_pos(self.t)

	# Debug

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

	world.set_time(0)

	print(world)
