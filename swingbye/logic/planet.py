from swingbye.cphysics import Planet as CPlanet
from swingbye.logic.mixins import PredictionMixin
from swingbye.globals import PLANET_PREDICTION_N

class Planet(CPlanet, PredictionMixin):
	def __init__(self, *args, **kwargs):
		CPlanet.__init__(self, *args, **kwargs)
		PredictionMixin.__init__(self, PLANET_PREDICTION_N)
