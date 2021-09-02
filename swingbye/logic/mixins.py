import numpy as np

class PredictionMixin:
	def __init__(self, nsamples: int):
		self.prediction = np.zeros((nsamples, 2))

	def _get_prediction(self):
		return self._prediction

	def _set_prediction(self, prediction: np.ndarray):
		self._prediction = prediction

	prediction = property(_get_prediction, _set_prediction)
