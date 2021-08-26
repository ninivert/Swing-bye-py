import pyglet
import glooey
from swingbye.pygletengine.utils import clamp


class Slider(glooey.Widget):
	custom_alignment = 'fill'
	custom_grab_mouse_on_click = True
	custom_base = pyglet.shapes.Rectangle
	custom_knob = pyglet.shapes.Circle

	def __init__(self, min_width=10, min_height=0, value=0, min_value=0, max_value=100, step=1, edge=0):
		super().__init__()
		
		self.min_width = min_width
		self.min_height = min_height

		self.base = None
		self.knob = None
		self.base_height = 10
		self.knob_size = 10

		self.captured = False

		self.value = value
		self.old_value = None
		self.min_value = min_value
		self.max_value = max_value
		self.step = step
		self.edge = edge

	def get_value_range(self):
		return self.max_value - self.min_value

	def get_closest_value(self, x, y):
		# At what level of the slider has the mouse been pressed
		progress = (x - (self.x + self.edge)) / self.slider_width
		# Exact value that the mouse is pointing at, offset by half a step
		exact_value = self.get_value_range() * progress - (self.step//2) + self.min_value
		remainder = abs(exact_value) % self.step;
		if remainder == 0:
			return exact_value
		if exact_value < 0:
			return -(abs(exact_value) - remainder)
		else:
			return exact_value + self.step - remainder

	def calculate_knob_position(self):
		return self.base.x + self.edge + ((self.slider_width - 2*self.edge)*((self.value - self.min_value) / self.get_value_range()))

	def load(self):
		self.x, self.y = self.get_rect().bottom_left
		self.slider_width = self.width - 2*self.horz_padding[0] - 2*self.knob_size
		if self.custom_base is not None:
			self.base = self.custom_base(0, 0, self.slider_width, self.base_height, batch=self.batch, group=self.group)
			self.base.x = self.x + self.horz_padding[0] + self.knob_size
			self.base.y = self.y + self.height//2 - self.base_height//2
		if self.custom_knob is not None:
			self.knob = self.custom_knob(0, 0, self.knob_size, batch=self.batch, group=self.group)

	def update_value(self, new_value):
		self.value = clamp(new_value, self.min_value, self.max_value)
		if self.value != self.old_value:
			self.dispatch_event('on_change', self, self.value)
			self.old_value = self.value
			self._draw()

	def reset(self):
		self.update_value(self.min_value)

	def do_claim(self):
		return self.min_width, self.min_height

	def do_resize(self):
		self.x, self.y = self.get_rect().bottom_left
		self.slider_width = self.width - 2*self.horz_padding[0] - 2*self.knob_size
		if self.base is not None:
			self.base.width = self.slider_width
			self.base.x = self.x + self.horz_padding[0] + self.knob_size
			self.base.y = self.y + self.height//2 - self.base_height//2

	def do_draw(self):
		if self.base is None or self.knob is None:
			self.load()

		self.knob.x = self.calculate_knob_position()
		self.knob.y = self.y + self.height//2
		
		self.base.visible = True
		self.knob.visible = True

	def do_undraw(self):
		if self.base is not None:
			self.base.visible = False
		if self.knob is not None:
			self.knob.visible = False

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		self.update_value(self.value + (self.step * scroll_y))

	def on_mouse_press(self, x, y, buttons, modifiers):
		self.update_value(self.get_closest_value(x, y))
		self.captured = True

	def on_mouse_release(self, x, y, buttons, modifiers):
		self.captured = False

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.captured:
			self.update_value(self.get_closest_value(x, y))


Slider.register_event_type('on_change')
