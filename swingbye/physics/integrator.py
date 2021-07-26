import numpy as np
import abc
from typing import Callable
from .entity import ImplicitEntity

class Integrator(abc.ABC):
	def __init__(self):
		pass

	@abc.abstractmethod
	def __call__(self, tiddy: ImplicitEntity, force_func: Callable[[ImplicitEntity, float], np.ndarray], t: float, dt: float) -> None:
		raise NotImplementedError()


class RK4Integrator(Integrator):
	def __init__(self):
		pass

	def __call__(self, tiddy: ImplicitEntity, force_func: Callable[[ImplicitEntity, float], np.ndarray], t: float, dt: float) -> None:
		# Special case for the N-body problem
		f_ti = force_func(tiddy, t)
		tiddy.x += tiddy.v * dt/2
		f_th = force_func(tiddy, t + dt/2)
		tiddy.x += tiddy.v * dt/2
		f_tf = force_func(tiddy, t + dt)
		tiddy.v += (1/6*f_ti + 4/6*f_th + 1/6*f_tf)/tiddy.m * dt


class EulerIntegrator(Integrator):
	def __init__(self):
		pass

	def __call__(self, tiddy: ImplicitEntity, force_func: Callable[[ImplicitEntity, float], np.ndarray], t: float, dt: float) -> None:
		tiddy.x += tiddy.v * dt
		tiddy.v += force_func(tiddy, t)/tiddy.m * dt
