import pyglet


class EventManager(pyglet.event.EventDispatcher):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		self.callbacks = {}
		self.capture_events()

	def capture_events(self):
		self.parent.push_handlers(self)

	def release_events(self):
		self.parent.remove_handlers(self)

	def on_mouse_motion(self, *args):
		if 'on_mouse_motion' in self.callbacks.keys():
			self.callbacks['on_mouse_motion'](*args)

	def on_mouse_press(self, *args):
		if 'on_mouse_press' in self.callbacks.keys():
			self.callbacks['on_mouse_press'](*args)

	def on_mouse_release(self, *args):
		if 'on_mouse_release' in self.callbacks.keys():
			self.callbacks['on_mouse_release'](*args)

	def on_mouse_scroll(self, *args):
		if 'on_mouse_scroll' in self.callbacks.keys():
			self.callbacks['on_mouse_scroll'](*args)

	def on_mouse_drag(self, *args):
		if 'on_mouse_drag' in self.callbacks.keys():
			self.callbacks['on_mouse_drag'](*args)

	def on_resize(self, *args):
		if 'on_resize' in self.callbacks.keys():
			self.callbacks['on_resize'](*args)
