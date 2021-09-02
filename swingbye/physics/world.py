import numpy as np
import logging
from dataclasses import dataclass, field
from typing import List, Union
from swingbye.physics.entity import ImplicitEntity
from swingbye.physics.ship import Ship
from swingbye.physics.planet import Planet
from swingbye.physics.integrator import Integrator, EulerIntegrator
from swingbye.physics.globals import GRAVITY_CST, GRAVITY_SINGULARITY_OFFSET
from swingbye.globals import SHIP_PREDICTION_N, PLANET_PREDICTION_N, PLANET_PREDICTION_DT, PHYSICS_DT
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
			if d != 0:
				n = r/d
			else:
				n = np.zeros(2)
			f += GRAVITY_CST*(titty.mass + planet.mass)/(d+GRAVITY_SINGULARITY_OFFSET)**2 * n

		return f

	def step(self, dt: float):
		if not self.ship.docked:
			self.integrator.integrate(self.ship, self.get_forces_on, self.time, dt)
			self.time += dt

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

		if self.ship.docked:
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
		self.update_ship_prediction()

	def update_ship_prediction(self):
		if not self.ship.docked:
			_logger.warning('ship prediction doesn\'t need to be updated since ship is launched')
			return

		temp_ship = Ship(parent=self.ship.parent, time=self.ship.time, pointing=self.ship.pointing)  # create a copy
		temp_ship.launch()

		for i, t in enumerate(np.linspace(self.time, self.time + (self.ship.prediction.shape[0]-1)*PHYSICS_DT, self.ship.prediction.shape[0])):
			self.ship.prediction[i, :] = temp_ship.pos
			self.integrator.integrate(temp_ship, self.get_forces_on, t, PHYSICS_DT)

		self.ship.prediction = self.ship.prediction

	def update_planets_prediction(self):
		for planet in self.planets:
			for i, t in enumerate(np.linspace(self.time, self.time + planet.prediction.shape[0]*PLANET_PREDICTION_DT, planet.prediction.shape[0])):
				planet.prediction[i, :] = planet.pos_at(t)  # Doesn't call the setter

			planet.prediction = planet.prediction  # HACK : update the vertices in swingbye.pygletengine.gameobjects.utils.PathMixin

	# Energy

	def kinetic_energy(self):
		return 0.5 * np.linalg.norm(self.ship.vel)**2 * self.ship.mass

	def potential_energy(self):
		u = 0
		for planet in self.planets:
			u += -GRAVITY_CST * planet.mass * self.ship.mass / np.linalg.norm(planet.pos - self.ship.pos)
		return u

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
