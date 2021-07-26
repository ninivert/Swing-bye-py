import numpy as np
from math import *
import logging
from .entity import ExplicitEntity
from .globals import EPSILON_EULER, MAX_ITER_EULER, GRAVITY_CST

_logger = logging.getLogger(__name__)

class Planet(ExplicitEntity):
	def __init__(
		self,
		x: np.ndarray = np.zeros(2),  # position
		m: float = 1,   # m@ss
		s: float = 1,  # semi-major axis
		e: float = 0,  # eccentricity
		t0: float = 0,  # initial time offset
		i: float = 0,  # inclination
		w: float = 0,  # argument of periaxis
		parent=None  # parent planet
	):
		self.s = s
		self.e = e
		self.t0 = t0
		self.i = i
		self.w = w
		self.parent = parent
		super().__init__(x, m)

	def get_vel(self, t: float) -> np.ndarray:
		dt = 0.016666
		return (self.get_pos(t+dt/2)-self.get_pos(t-dt/2))/dt

	def get_pos(self, t: float) -> np.ndarray:
		if self.parent is None:
			return self.x

		x = np.zeros(2)
		p = self.parent
		while p is not None:
			x += p.get_pos(t)
			p = p.parent

		mu = GRAVITY_CST*(self.m + self.parent.m)

		if 0 <= self.e and self.e < 1:
			T = sqrt(4 * pi**2 * self.s**3 / mu)
			tau = fmod(t - self.t0, T)
			n = 2*pi/T
			M = n*tau
			E = M
			dE = EPSILON_EULER + 1
			i: int = 0

			# Solve M = E - e*sin(E)
			while abs(dE) > EPSILON_EULER and i < MAX_ITER_EULER:
				dE = (M - E + self.e*sin(E))/(1 - self.e * cos(E))
				E += dE
				i += 1
			if i == MAX_ITER_EULER:
				_logger.warning(f'Euler equation solving did not escape after {MAX_ITER_EULER} iterations.')

			costheta = (cos(E) - self.e)/(1 - self.e*cos(E))
			sintheta = (sqrt(1 - self.e**2) * sin(E))/(1 - self.e*cos(E))
			r = self.s * (1 - self.e*cos(E))

		elif 1 < self.e:
			tau = t - t0
			n = sqrt(-mu/self.s**3)
			M = n*tau
			H = M
			dH = EPSILON_EULER + 1
			i: int = 0

			# Solve M = e*sinh(H) - H
			while abs(dH) > EPSILON_EULER and i < MAX_ITER_EULER:
				dH = (M - self.e*sinh(H) + H)/(self.e*cosh(H) - 1)
				H += dH
				i += 1
			if i == MAX_ITER_EULER:
				_logger.warning(f'Euler equation solving did not escape after {MAX_ITER_EULER} iterations.')

			r = self.s * (1 - self.e*cosh(H))
			costheta = (self.e - cosh(H))/(self.e*cosh(H) - 1)
			sintheta = sign(H)*sin(acos(costheta))

		rel_x = np.zeros(2)
		rel_x[0] = r*costheta
		rel_x[1] = r*sintheta

		# Argument of periaxis
		pog = rel_x[0]
		champ = rel_x[1]
		rel_x[0] = pog*cos(self.w) - champ*sin(self.w) 
		rel_x[1] = pog*sin(self.w) + champ*cos(self.w)
		# Inclination
		rel_x[0] *= cos(i)

		return x + rel_x

	def __str__(self):
		ret = super().__str__()
		ret += f'\n\tpos {self._x}, mass {self._m}, parent {self.parent}'
		return ret
