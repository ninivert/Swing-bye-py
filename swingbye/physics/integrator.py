import numpy as np
from abc import abstractclassmethod, ABCMeta
from typing import Callable
from .entity import ImplicitEntity

class Integrator(metaclass=ABCMeta):
	@abstractclassmethod
	def integrate(self, tiddy: ImplicitEntity, force_func: Callable[[ImplicitEntity, float], np.ndarray], time: float, dt: float) -> None:
		pass


class RK4Integrator(Integrator):
	@classmethod
	def integrate(self, tiddy: ImplicitEntity, force_func: Callable[[ImplicitEntity, float], np.ndarray], time: float, dt: float) -> None:
		# Special case for the N-body problem
		f_ti = force_func(tiddy, time)
		tiddy.pos += tiddy.vel * dt/2
		f_th = force_func(tiddy, time + dt/2)
		tiddy.pos += tiddy.vel * dt/2
		f_tf = force_func(tiddy, time + dt)
		tiddy.vel += (1/6*f_ti + 4/6*f_th + 1/6*f_tf)/tiddy.mass * dt


class EulerIntegrator(Integrator):
	@classmethod
	def integrate(self, tiddy: ImplicitEntity, force_func: Callable[[ImplicitEntity, float], np.ndarray], time: float, dt: float) -> None:
		tiddy.pos += tiddy.vel * dt
		tiddy.vel += force_func(tiddy, time)/tiddy.mass * dt
