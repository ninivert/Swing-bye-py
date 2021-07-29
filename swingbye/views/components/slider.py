import pyglet


class Base(pyglet.shapes.Rectangle):
	base_color = (255, 255, 255)
	over_color = (220, 220, 220)
	down_color = (180, 180, 180)

	def __init__(self, x, y, width, height, *args, **kwargs):
		super().__init__(x, y, width, height, *args, color=self.base_color, **kwargs)

	def hit(self, x, y):
		return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)

	def slider_base(self):
		self.color = self.base_color

	def over(self):
		self.color = self.over_color

	def down(self):
		self.color = self.down_color


class Knob(pyglet.shapes.Circle):
	base_color = (255, 255, 255)
	over_color = (220, 220, 220)
	down_color = (180, 180, 180)

	def __init__(self, x, y, radius, *args, **kwargs):
		super().__init__(x, y, radius, *args, color=self.base_color, **kwargs)

	def hit(self, x, y):
		return ((x - self.x)**2 + (y - self.y)**2)**0.5 <= self.radius

	def slider_base(self):
		self.color = self.base_color

	def over(self):
		self.color = self.over_color

	def down(self):
		self.color = self.down_color


class Slider:

	def __init__(self, x, y, slider_base, slider_knob, value=0, min_value=0, max_value=100, step=1, edge=0, parent=None):
		self.updated = True
		self.hovering = False
		self.captured = False

		self._x = x
		self._y = y
		self.width = slider_base.width
		self.height = slider_base.height // 2
		self.slider_width = self.width - 2 * edge

		slider_base.position = x, y
		slider_knob.position = x+edge, y+(slider_base.height//2)

		self.slider_base = slider_base
		self.slider_knob = slider_knob
		self._value = value
		self._old_value = value
		self.min_value = min_value
		self.max_value = max_value
		self.step = step
		self.edge = edge
		self.parent = parent

	@property
	def value(self):
		self.updated = False
		return self._value

	@value.setter
	def value(self, value):
		if self.min_value <= value <= self.max_value:
			self._value = value
			self.update()
		else:
			print('sdfvghjksdfgbhjksdfgvhbjnk')

	@property
	def x(self):
		return self._x

	@value.setter
	def x(self, x):
		self._x = x
		self.slider_knob.x = self.calculate_knob_position()
		self.slider_base.x = x

	@property
	def y(self):
		return self._y

	@value.setter
	def y(self, y):
		self._y = y
		self.slider_knob.y = y + (self.height // 2)
		self.slider_base.y = y

	def attach_parent(self, parent):
		self.parent = parent

	def detach_parent(self):
		self.parent = None

	def base(self):
		self.slider_knob.slider_base()
		self.slider_base.slider_base()

	def over(self):
		self.slider_knob.over()
		self.slider_base.over()

	def down(self):
		self.slider_knob.down()
		self.slider_base.down()

	def hit(self, x, y):
		return self.slider_knob.hit(x, y) or self.slider_base.hit(x, y)

	def get_value_range(self):
		return self.max_value - self.min_value

	def get_closest_value(self, x, y):
		progress = (x - self._x - self.edge) / self.slider_width
		exact_value = self.get_value_range() * progress - (self.step//2)
		remainder = abs(exact_value) % self.step;
		if remainder == 0:
			return exact_value
		if exact_value < 0:
			return -(abs(exact_value) - remainder)
		else:
			return exact_value + self.step - remainder

	def calculate_knob_position(self):
		return self._x + self.edge + (self.slider_width*((self._value - self.min_value) / self.get_value_range()))

	def clamp(self, value):
		return min(max(value, self.min_value), self.max_value)

	def update(self):
		self.slider_knob.x = self.calculate_knob_position()
		
		if self._value != self._old_value:
			self.updated = True
			self._old_value = self._value

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if self.hit(x, y):
			self._value = self.clamp(self._value + (self.step * scroll_y))

	def on_mouse_press(self, x, y, buttons, modifiers):
		if self.hit(x, y):
			self._value = self.clamp(self.get_closest_value(x, y))
			self.captured = True
			self.down()

	def on_mouse_release(self, x, y, buttons, modifiers):
		self.captured = False
		if self.hit(x, y):
			self.hovering = True
			self.over()
		else:
			self.hovering = False
			self.base()

	def on_mouse_motion(self, x, y, dx, dy):
		if not self.captured:
			if self.hit(x, y):
				self.hovering = True
				self.over()
			else:
				self.hovering = False
				self.base()

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.captured:
			self._value = self.clamp(self.get_closest_value(x, y))
