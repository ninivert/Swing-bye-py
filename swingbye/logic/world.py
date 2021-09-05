import logging
import numpy
from swingbye.cphysics import World as CWorld
from swingbye.cphysics import vec2
from swingbye.globals import PLANET_PREDICTION_DT, PHYSICS_DT, SHIP_LAUNCH_SPEED
from enum import Enum, auto
from typing import Optional

_logger = logging.getLogger(__name__)

class WorldStates(Enum):
	PRE_LAUNCH = auto()
	POST_LAUNCH = auto()

class World(CWorld):
	def __init__(self):
		CWorld.__init__(self)
		self.state = WorldStates.PRE_LAUNCH
		self.autoupdate_predictions = True
		self.time = 0.0

	# Time handling

	def _get_time(self):
		return CWorld._get_time(self)

	def _set_time(self, time: float):
		CWorld._set_time(self, time)  # internally sets the time, moving planets around in c++

		for ship in self.entities:
			ship.time = time  # ship subclasses cphysics.Entity to have a time property
			ship.pos = ship.pos  # HACK : trigger the position setter
			ship.vel = ship.vel  # HACK : trigger the position setter

		for planet in self.planets:
			planet.pos = planet.pos  # HACK : trigger the position setter

		if self.autoupdate_predictions:
			self.update_predictions()

	time = property(_get_time, _set_time)

	def step(self, dt, update_predictions=Optional[bool]):
		# prevent updating if not requested
		if update_predictions is not None:
			old_autoupdate_predictions = self.autoupdate_predictions
			self.autoupdate_predictions = update_predictions

		CWorld.step(self, dt)
		self.time = self.time  # HACK : trigger the time setter

		# restore state
		self.autoupdate_predictions = old_autoupdate_predictions

	# Game logic

	def launch_ship(self):
		self.ship.launch()
		self.state = WorldStates.POST_LAUNCH

	def point_ship(self, clickpos):
		if not self.ship.docked:
			return

		pointing = clickpos - self.ship.parent.pos
		pointing_norm = pointing.length()

		if pointing_norm == 0.0:
			_logger.warning('pointing click happened on ship, cannot determine pointing vector, ignoring')
			return

		pointing /= pointing_norm

		self.ship.pointing = pointing
		self.update_ships_prediction()

	def update_predictions(self):
		self.update_ships_prediction()
		self.update_planets_prediction()

	def update_ships_prediction(self):
		for ship in self.entities:
			# if not ship.docked:
			# 	_logger.warning('ship prediction doesn\'t need to be updated since ship is launched')
			# 	return

			# TODO : prevent copy by STL vector -> numpy array
			if ship.docked:
				old_vel = self.ship.vel
				self.ship.vel = self.ship.pointing*(SHIP_LAUNCH_SPEED + self.ship.parent.vel.length())
				c_prediction = self.get_predictions(self.ship, self.time, self.time + (self.ship.prediction.shape[0]-1)*PHYSICS_DT, self.ship.prediction.shape[0])
				self.ship.vel = old_vel
			else:
				c_prediction = self.get_predictions(self.ship, self.time, self.time + (self.ship.prediction.shape[0]-1)*PHYSICS_DT, self.ship.prediction.shape[0])

			for i, sample in enumerate(c_prediction):
				ship.prediction[i, :] = tuple(sample)

			ship.prediction = ship.prediction

	def update_planets_prediction(self):
		for planet in self.planets:
			for i, t in enumerate(numpy.linspace(self.time, self.time + planet.prediction.shape[0]*PLANET_PREDICTION_DT, planet.prediction.shape[0])):
				planet.prediction[i, :] = tuple(planet.pos_at(t))  # Doesn't call the setter

			planet.prediction = planet.prediction  # HACK : update the vertices in swingbye.pygletengine.gameobjects.utils.PathMixin

	@property
	def ship(self):
		if len(self.entities) > 0:
			return self.entities[0]  # lol
		else:
			_logger.warning('requested ship, but there is none in world')
			return None
