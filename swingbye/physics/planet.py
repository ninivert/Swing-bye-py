import numpy as np
import logging
import math
from dataclasses import dataclass
from typing import Union
from .entity import ExplicitEntity
from .globals import EPSILON_EULER, MAX_ITER_EULER, GRAVITY_CST
from ..globals import PLANET_PREDICTION_N, PLANET_PREDICTION_DT

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

		mu = GRAVITY_CST*(self.mass + self.parent.mass)

		if 0 <= self.ecc and self.ecc < 1:
			T = math.sqrt(4 * math.pi**2 * self.maxis**3 / mu)
			tau = math.fmod(time - self.time0, T)
			n = 2*math.pi/T
			M = n*tau
			E = M
			dE = EPSILON_EULER + 1
			i = 0

			# Solve M = E - e*sin(E)
			while abs(dE) > EPSILON_EULER and i < MAX_ITER_EULER:
				dE = (M - E + self.ecc*math.sin(E))/(1 - self.ecc * math.cos(E))
				E += dE
				i += 1
			if i >= MAX_ITER_EULER:
				_logger.warning(f'Euler equation solving did not escape after {MAX_ITER_EULER} iterations.')

			costheta = (math.cos(E) - self.ecc) / (1 - self.ecc*math.cos(E))
			sintheta = (math.sqrt(1 - self.ecc**2) * math.sin(E)) / (1 - self.ecc*math.cos(E))
			r = self.maxis * (1 - self.ecc*math.cos(E))

		elif 1 < self.ecc:
			tau = time - self.time0
			n = math.sqrt(-mu/self.maxis**3)
			M = n*tau
			H = M
			dH = EPSILON_EULER + 1
			i = 0

			# Solve M = e*sinh(H) - H
			while abs(dH) > EPSILON_EULER and i < MAX_ITER_EULER:
				dH = (M - self.ecc*math.sinh(H) + H) / (self.ecc*math.cosh(H) - 1)
				H += dH
				i += 1
			if i >= MAX_ITER_EULER:
				_logger.warning(f'Euler equation solving did not escape after {MAX_ITER_EULER} iterations.')

			r = self.maxis * (1 - self.ecc*math.cosh(H))
			costheta = (self.ecc - math.cosh(H)) / (self.ecc*math.cosh(H) - 1)
			sintheta = math.copysign(1, H)*math.sin(math.acos(costheta))

		pos[0] = r*costheta
		pos[1] = r*sintheta

		# Argument of periaxis
		posx = pos[0]
		posy = pos[1]
		pos[0] = posx*math.cos(self.parg) - posy*math.sin(self.parg)
		pos[1] = posx*math.sin(self.parg) + posy*math.cos(self.parg)

		# Inclination
		pos[0] *= np.cos(self.incl)

		return pos

	def vel_at(self, time: float) -> np.ndarray:
		dt = 0.016666
		return (self.pos_at(time+dt/2)-self.pos_at(time-dt/2))/dt

	@property
	def predicted(self):
		# TODO : add dirty state
		predicted = np.zeros((PLANET_PREDICTION_N, 2))

		for i, t in enumerate(np.linspace(self._t, self._t + PLANET_PREDICTION_N*PLANET_PREDICTION_DT, PLANET_PREDICTION_N)):
			predicted[i, :] = self.pos_at(self, t)

		return predicted


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
