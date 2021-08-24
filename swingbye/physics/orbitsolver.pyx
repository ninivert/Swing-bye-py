from swingbye.physics.globals import EPSILON_EULER, MAX_ITER_EULER, GRAVITY_CST
import logging
import cython
import math

_logger = logging.getLogger(__name__)

cdef double _EPSILON_EULER = EPSILON_EULER
cdef double _GRAVITY_CST = GRAVITY_CST
cdef unsigned int _MAX_ITER_EULER = MAX_ITER_EULER

cpdef (double, double) solve_orbit(double time, double mass, double pmass, double ecc, double maxis, double time0, double parg, double incl):
	cdef double x = 0.0
	cdef double y = 0.0
	cdef double mu = _GRAVITY_CST*(mass + pmass)

	cdef double costheta, sintheta, r
	cdef double T, tau, n, M
	cdef double E, dE
	cdef unsigned int i

	if 0 <= ecc and ecc < 1:
		T = math.sqrt(4 * math.pi**2 * maxis**3 / mu)
		tau = math.fmod(time - time0, T)
		n = 2*math.pi/T
		M = n*tau
		E = M
		dE = EPSILON_EULER + 1
		i = 0

		# Solve M = E - e*sin(E)
		while abs(dE) > _EPSILON_EULER and i < _MAX_ITER_EULER:
			dE = (M - E + ecc*math.sin(E))/(1 - ecc * math.cos(E))
			E += dE
			i += 1
		if i >= MAX_ITER_EULER:
			_logger.warning(f'Euler equation solving did not escape after {_MAX_ITER_EULER} iterations.')

		costheta = (math.cos(E) - ecc) / (1 - ecc*math.cos(E))
		sintheta = (math.sqrt(1 - ecc**2) * math.sin(E)) / (1 - ecc*math.cos(E))
		r = maxis * (1 - ecc*math.cos(E))

	elif 1 < ecc:
		tau = time - time0
		n = math.sqrt(-mu/maxis**3)
		M = n*tau
		E = M
		dE = EPSILON_EULER + 1
		i = 0

		# Solve M = e*sinh(E) - E
		while abs(dE) > _EPSILON_EULER and i < _MAX_ITER_EULER:
			dE = (M - ecc*math.sinh(E) + E) / (ecc*math.cosh(E) - 1)
			E += dE
			i += 1
		if i >= MAX_ITER_EULER:
			_logger.warning(f'Euler equation solving did not escape after {_MAX_ITER_EULER} iterations.')

		r = maxis * (1 - ecc*math.cosh(E))
		costheta = (ecc - math.cosh(E)) / (ecc*math.cosh(E) - 1)
		sintheta = math.copysign(1, E)*math.sin(math.acos(costheta))

	x = r*costheta
	y = r*sintheta

	# Argument of periaxis
	x_temp = x
	x = x*math.cos(parg) - y*math.sin(parg)
	y = x_temp*math.sin(parg) + y*math.cos(parg)

	# Inclination
	x *= math.cos(incl)

	return (x, y)
