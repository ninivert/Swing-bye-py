import numpy as np
import logging
from dataclasses import dataclass, field
from typing import Union
from swingbye.physics.entity import ExplicitEntity
from swingbye.physics.orbitsolver import solve_orbit
from swingbye.globals import PLANET_PREDICTION_N

_logger = logging.getLogger(__name__)

@dataclass
class Planet(ExplicitEntity):
	# Semi-major axis
	maxis: float = 1.0
	# Eccentricity
	ecc: float = 0.0
	# Initial time offset
	time0: float = 0.0
	# Inclination
	incl: float = 0.0
	# Argument of periaxis
	parg: float = 0.0
	# Planet radius
	radius: float = 0.0
	# Parent
	# NOTE : type hint is `'Planet'` instead of `Planet`,
	# since the class is not defined at this point
	parent: Union[None, 'Planet'] = None
	# Prediction
	prediction: np.ndarray
	_prediction: np.ndarray = field(init=False, repr=False, default=np.zeros((PLANET_PREDICTION_N, 2)))

	# Position solver

	def pos_at(self, time: float) -> np.ndarray:
		pos = np.zeros(2)
		parent = self

		while parent is not None:
			pos += parent.rel_pos_at(time)
			if parent.parent is None:
				pos += parent.anchor
			parent = parent.parent

		return pos

	def rel_pos_at(self, time: float) -> np.ndarray:
		pos = np.zeros(2)

		if self.parent is None:
			return pos

		return np.array(solve_orbit(time, self.mass, self.parent.mass, self.ecc, self.maxis, self.time0, self.parg, self.incl))

	# Velocity hack

	def vel_at(self, time: float) -> np.ndarray:
		dt = 0.016666
		return (self.pos_at(time+dt/2)-self.pos_at(time-dt/2))/dt

	# Prediction

	def _get_prediction(self):
		return self._prediction

	def _set_prediction(self, prediction):
		if type(prediction) is property:
			prediction = Planet._prediction

		self._prediction = prediction

	prediction = property(_get_prediction, _set_prediction)


if __name__ == '__main__':
	p1 = Planet(anchor=np.array([2.0, 3.0]))
	p2 = Planet(parent=p1, maxis=5.0)
	p3 = Planet(parent=p2, maxis=2.0, radius=0.3)

	print('>>> initialized planets')
	print(p1, p2, p3, sep='\n')

	print('>>> positions at time 0')
	print(p1.pos_at(0))
	print(p2.pos_at(0))
	print(p3.pos_at(0))

	print('>>> positions at time 1')
	print(p1.pos_at(1))
	print(p2.pos_at(1))
	print(p3.pos_at(1))
