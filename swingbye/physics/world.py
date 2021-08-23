import numpy as np
import logging
import dataclasses
from dataclasses import dataclass, field
from typing import List, Union
from .entity import ImplicitEntity
from .ship import Ship
from .planet import Planet
from .globals import GRAVITY_CST, GRAVITY_SINGULARITY_OFFSET
from ..globals import SHIP_PREDICTION_N, SHIP_PREDICTION_DT, PLANET_PREDICTION_N, PLANET_PREDICTION_DT
from .integrator import Integrator, EulerIntegrator
from enum import Enum, auto

_logger = logging.getLogger(__name__)

class WorldStates(Enum):
	PRE_LAUNCH = auto()
	POST_LAUNCH = auto()

@dataclass
class World():
	planets: List[Planet] = field(default_factory=list)
	ship: Union[Ship, None] = None
	integrator: Integrator = EulerIntegrator
	time: float
	_time: float = field(init=False, repr=False, default=0.0)
	state: WorldStates = WorldStates.PRE_LAUNCH

	# Physics

	def get_forces_on(self, titty: ImplicitEntity, time: float = None):
		if time is None:
			time = self.time

		f = np.zeros(2)
		for planet in self.planets:
			r = planet.pos_at(time) - titty.pos
			d = np.linalg.norm(r)
			n = r/d
			f += GRAVITY_CST*(titty.mass + planet.mass)/(d+GRAVITY_SINGULARITY_OFFSET)**2 * n

		return f

	def step(self, dt: float):
		if not self.ship.docked:
			self.time += dt
			self.integrator.integrate(self.ship, self.get_forces_on, self.time, dt)

	# Time handling

	@property
	def time(self):
		return self._time

	@time.setter
	def time(self, time: float):
		if type(time) is property:
			time = World._time

		self._time = time

		for planet in self.planets:
			planet.time = time
			# position is updated lazily for planets, so we call planet.pos to resolve it and force an update
			# this should normally not be needed, but since we are drawing every frame the sprite positions need to be updated
			planet.pos

		self.ship.time = time

		self.update_ship_prediction()
		self.update_planets_prediction()

	# Game logic

	def launch_ship(self):
		self.state = WorldStates.POST_LAUNCH
		self.ship.launch()

	def point_ship(self, clickpos: np.ndarray):
		if not self.ship.docked:
			return

		pointing = clickpos - self.ship.parent.pos
		pointing_norm = np.linalg.norm(pointing)

		if pointing_norm == 0.0:
			_logger.warning('pointing click happened on ship, cannot determine pointing vector, ignoring')
			return

		pointing /= pointing_norm

		self.ship.pointing = pointing

	def update_ship_prediction(self):
		if not self.ship.docked:
			_logger.warning('ship prediction doesn\'t need to be updated since ship is launched')

		temp_ship = dataclasses.replace(self.ship)
		temp_ship.launch()

		for i, t in enumerate(np.linspace(self.time, self.time + SHIP_PREDICTION_N*SHIP_PREDICTION_DT, SHIP_PREDICTION_N)):
			self.integrator.integrate(temp_ship, self.get_forces_on, t, SHIP_PREDICTION_DT)
			self.ship.predicted[i, :] = temp_ship.pos

	def update_planets_prediction(self):
		for planet in self.planets:
			# predicted = np.zeros((PLANET_PREDICTION_N, 2))

			for i, t in enumerate(np.linspace(self.time, self.time + PLANET_PREDICTION_N*PLANET_PREDICTION_DT, PLANET_PREDICTION_N)):
				planet.predicted[i, :] = self.pos_at(self, t)

			# planet.predicted = predicted

	# Debug

	def __str__(self):
		res = super().__str__()
		res += '\n\t| ' + self.ship.__str__()
		for planet in self.planets:
			res += '\n\t| ' + planet.__str__()
		return res


if __name__ == '__main__':
	from .integrator import EulerIntegrator, RK4Integrator

	for integrator in [EulerIntegrator, RK4Integrator]:
		print(f'>>> using integrator {integrator}')

		world = World(
			ship=Ship(pos=np.array([100.0, 100.0])),
			planets=[
				p1 := Planet(anchor=np.array([2.0, 3.0])),
				p2 := Planet(parent=p1, maxis=5.0),
				p3 := Planet(parent=p2, maxis=2.0, radius=0.3)
			],
			integrator=integrator
		)

		print('>>> world after initialization')
		print(world)

		print('>>> stepping 4 times by 0.1')
		world.step(0.1)
		world.step(0.1)
		world.step(0.1)
		world.step(0.1)

		print(world)
		# print(world.planets[2].pos)

		print('>>> setting time to 0')
		world.time = 0

		print(world)
