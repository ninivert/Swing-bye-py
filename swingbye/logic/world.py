import logging
import numpy as np
from swingbye.cphysics import World as CWorld
from swingbye.cphysics import vec2
from swingbye.globals import PLANET_PREDICTION_DT, PHYSICS_DT
from enum import Enum, auto

_logger = logging.getLogger(__name__)

class WorldStates(Enum):
	PRE_LAUNCH = auto()
	POST_LAUNCH = auto()

class World(CWorld):
	def __init__(self):
		self.time = 0.0

	# Time handling

	def _get_time(self):
		return self._time

	def _set_time(self, time: float):
		self._time = time

		for planet in self.planets:
			planet.time = time

		for ship in self.entities:
			ship.time = time

		if self.ship.docked:
			self.update_ship_prediction()
		self.update_planets_prediction()

	time = property(_get_time, _set_time)

	# Game logic

	def launch_ship(self):
		self.ship.launch()
		self.state = WorldStates.POST_LAUNCH

	def point_ship(self, clickpos: vec2):
		if not self.ship.docked:
			return

		pointing = clickpos - self.ship.parent.pos
		pointing_norm = pointing.length()

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

		c_prediction = self.get_predictions(self.ship, self.time, self.time + (self.ship.prediction.shape[0]-1)*PHYSICS_DT, self.ship.prediction.shape[0])

		for i, sample in enumerate(c_prediction):
			self.ship.prediction[i, :] = sample.to_tuple()

		self.ship.prediction = self.ship.prediction

	def update_planets_prediction(self):
		for planet in self.planets:
			for i, t in enumerate(np.linspace(self.time, self.time + planet.prediction.shape[0]*PLANET_PREDICTION_DT, planet.prediction.shape[0])):
				planet.prediction[i, :] = planet.pos_at(t)  # Doesn't call the setter

			planet.prediction = planet.prediction  # HACK : update the vertices in swingbye.pygletengine.gameobjects.utils.PathMixin

	@property
	def ship(self):
		return self.entities[0]  # lol
