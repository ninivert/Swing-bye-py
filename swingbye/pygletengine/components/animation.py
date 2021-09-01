import glooey
import pyglet


class AnimationWidget(glooey.Widget):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.animation = None
		self.elapsed_time = 0

	def do_detach(self):
		self.stop_animation()

	def _update(self, dt, *args, **kwargs):
		self.elapsed_time += dt
		self.update(dt, *args, **kwargs)
		if self.animation.done:
			self.stop_animation()

	def update(self, dt, *args, **kwargs):
		raise NotImplementedError('abstract')

	def start_animation(self, *args, **kwargs):
		if self.animation is not None:
			self.reset_animation()
			pyglet.clock.unschedule(self._update)
			pyglet.clock.schedule_interval(self._update, 1 / 60, *args, **kwargs)

	def stop_animation(self):
		pyglet.clock.unschedule(self._update)

	def reset_animation(self):
		self.animation.reset()


# should this be an EventDispatcher so it can emit an 'on_animation_end'?
class Animation:

	def __init__(self, keyframes, repeat=False):
		self._keyframes = keyframes
		self.elapsed_time = 0
		self.total_duration = self.get_total_duration()

		self.done = False
		self.repeat = repeat

	@property
	def keyframes(self):
		return self._keyframes[:]

	@keyframes.setter
	def keyframes(self, keyframes):
		self._keyframes = keyframes
		self.total_duration = self.get_total_duration()

	def reset(self):
		self.done = False
		self.elapsed_time = 0

	def get_total_duration(self):
		duration = 0
		for keyframe in self._keyframes:
			duration += keyframe.duration
		return duration

	def get_next_value(self, dt):
		self.elapsed_time += dt
		if self.elapsed_time > self.total_duration:
			if self.repeat:
				self.elapsed_time = 0
			else:
				self.done = True
		if not self.done:
			value = None
			cumulated = 0
			for keyframe in self._keyframes:
				if cumulated + keyframe.duration > self.elapsed_time:
					value = keyframe.get_next_value(self.elapsed_time - cumulated)
					break
				cumulated += keyframe.duration
			return value
		else:
			return self._keyframes[-1].end_value


class Keyframe:

	def __init__(self, start_value, end_value, duration, smoothing_func):
		self.start_value = start_value
		self.end_value = end_value
		self.duration = duration
		self.smoothing_func = smoothing_func

	def get_next_value(self, elapsed_time):
		return self.smoothing_func(self.start_value, self.end_value, elapsed_time / self.duration)