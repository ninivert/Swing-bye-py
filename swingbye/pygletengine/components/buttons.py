import pyglet
import glooey
from glooey.drawing.color import hex_to_int
import numpy as np
import swingbye.pygletengine.components.theme as theme
from swingbye.pygletengine.components.labels import ButtonLabel, Description
from swingbye.pygletengine.utils import clamp


class Button(glooey.Button):
	Foreground = ButtonLabel
	custom_alignment = 'fill'
	custom_background_layer = 1
	custom_foreground_layer = 2

	def __init__(self, label, callback=None, *args, **kwargs):
		super().__init__(label, *args, **kwargs)
		self.callback = callback

	def on_click(self, widget):
		if self.callback is not None:
			self.callback()

	def do_regroup_children(self):
		back = pyglet.graphics.OrderedGroup(self.custom_background_layer, parent=self.group)
		front = pyglet.graphics.OrderedGroup(self.custom_foreground_layer, parent=self.group)
		self._background._regroup(back)
		self._foreground._regroup(front)

	class Base(glooey.Background):
		custom_color = theme.BUTTON_BASE

	class Over(glooey.Background):
		custom_color = theme.BUTTON_OVER

	class Down(glooey.Background):
		custom_color = theme.BUTTON_DOWN


class SmallButton(Button):
	Foreground = Description


class MainMenuButton(glooey.Widget):
	custom_foreground_layer = 3
	custom_alignment = 'fill'
	custom_padding = 40

	def __init__(self, text, callback=None, radius=20, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._text = text
		self.background = None
		self.overlay = None
		self.foreground = ButtonLabel(text=self._text)

		self.radius = radius
		self.mouse_over = False
		self.mouse_change = False

		self.callback = callback

		self.total_time = 0
		self.animation_start = 0
		self.animation_time = 0.3
		
		self.loaded = False

		self._attach_child(self.foreground)

	@property
	def text(self):
		return self._text

	@text.setter
	def text(self, new_text):
		self._text = new_text
		self.foreground.text = new_text

	def load(self):
		self.background = pyglet.shapes.Circle(
			*self.rect.center,
			self.radius,
			color=hex_to_int(theme.BUTTON_BASE)[:3],
			batch=self.batch,
			group=pyglet.graphics.OrderedGroup(1, parent=self.group)
		)
		self.overlay = pyglet.shapes.Circle(
			*self.rect.center,
			0,
			color=hex_to_int(theme.MAIN_MENU_SLIDOVER)[:3],
			batch=self.batch,
			group=pyglet.graphics.OrderedGroup(2, parent=self.group)
		)
		self.loaded = True

	def do_draw(self):
		if not self.loaded:
			self.load()

	def do_undraw(self):
		if self.loaded:
			self.overlay.delete()
			self.background.delete()
			self.overlay = None
			self.background = None
			pyglet.clock.unschedule(self.update)
			self.loaded = False

	def do_claim(self):
		width = max(self.foreground.claimed_width, self.radius*2)
		height = max(self.foreground.claimed_height, self.radius*2)
		return width, height

	def do_regroup_children(self):
		self.foreground._regroup(pyglet.graphics.OrderedGroup(3, parent=self.group))

	def _resize(self, rect):
		super()._resize(rect)
		if self.loaded:
			self.background.x, self.background.y = self.rect.center
			self.overlay.x, self.overlay.y = self.rect.center

	def on_click(self, widget):
		if self.callback is not None:
			if self.mouse_over:
				self.callback()

	def on_mouse_enter(self, x, y):
		# Overide default to prevent rollover event
		return pyglet.event.EVENT_HANDLED

	def on_mouse_leave(self, x, y):
		if self.mouse_over:
			self.on_rollover(self, 'base', 'over')

	def on_mouse_motion(self, x, y, dx, dy):
		new_over = np.linalg.norm(np.array((x, y)) - np.array((self.rect.center_x, self.rect.center_y))) < self.radius
		self.mouse_change = new_over ^ self.mouse_over
		self.mouse_over = new_over
		if self.mouse_over and self.mouse_change:
			self.on_rollover(self, 'over', 'base')
		elif not self.mouse_over and self.mouse_change:
			self.on_rollover(self, 'base', 'over')

	def on_rollover(self, widget, new, old):
		if self.loaded:
			if new == 'over' and old == 'base':
				self.overlay.radius = 0
				self.overlay.color = hex_to_int(theme.MAIN_MENU_SLIDOVER)[:3]
				self.animation_start = self.total_time
				pyglet.clock.unschedule(self.update)
				pyglet.clock.schedule_interval(self.update, 1/60, direction=1)
			if new == 'base':
				self.overlay.color = hex_to_int(theme.MAIN_MENU_SLIDOVER)[:3]
				self.animation_start = self.total_time
				pyglet.clock.unschedule(self.update)
				pyglet.clock.schedule_interval(self.update, 1/60, direction=-1)
			if new == 'down':
				self.overlay.color = hex_to_int(theme.BUTTON_OVER)[:3]

	def update(self, dt, direction=1):
		self.total_time += dt
		easing = lambda a, b, t: a + ((b-a)*(1 - pow(1 - t, 3)))
		t = clamp((self.total_time - self.animation_start) / self.animation_time, 0, 1)
		if direction == 1:
			self.overlay.radius = easing(0, self.radius, t)
		elif direction == -1:
			self.overlay.radius = easing(self.radius, 0, t)
		if t == 1:
			pyglet.clock.unschedule(self.update)


class CycleButton(glooey.Button):
	Foreground = ButtonLabel
	custom_alignment = 'fill'

	def __init__(self, states, default=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.states = states
		self.state_names = list(self.states.keys())
		self.state_index = 0 if default is None else self.state_names.index(default)
		self.foreground.text = self.state_names[self.state_index]

	def on_click(self, widget):
		self.state_index = (self.state_index + 1) % len(self.states)
		self.foreground.text = self.state_names[self.state_index]
		self.dispatch_event('on_change', self, self.states[self.state_names[self.state_index]])

	def do_claim(self):
		max_x, max_y = 0, 0
		for text in self.state_names:
			test_label = self.Foreground(text)
			text_width, text_height = test_label.do_claim()
			max_x, max_y = max(max_x, text_width), max(max_y, text_height)
		return max_x, max_y
	
	class Base(glooey.Background):
		custom_color = theme.BUTTON_BASE

	class Over(glooey.Background):
		custom_color = theme.BUTTON_OVER

	class Down(glooey.Background):
		custom_color = theme.BUTTON_DOWN


CycleButton.register_event_type('on_change')


class SmallCycleButton(CycleButton):
	Foreground = Description