import pyglet
import glooey
from swingbye.pygletengine.components.labels import ButtonLabel, Description


class Button(glooey.Button):
	Foreground = ButtonLabel
	custom_alignment = 'fill'

	def __init__(self, label, callback=None, *args, **kwargs):
		super().__init__(label, *args, **kwargs)
		self.callback = callback

	def on_click(self, widget):
		if self.callback is not None:
			self.callback()

	class Base(glooey.Background):
		custom_color = '#aa1e1e'

	class Over(glooey.Background):
		custom_color = '#cc3f3f'

	class Down(glooey.Background):
		custom_color = '#ff5d5d'


class SmallButton(Button):
	Foreground = Description


class CycleButton(glooey.Button):
	Foreground = ButtonLabel
	custom_alignment = 'fill'

	def __init__(self, states, callback=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.states = states
		self.state_names = list(self.states.keys())
		self.state_index = 0
		self.callback = callback
		self.foreground.text = self.state_names[self.state_index]

	def on_click(self, widget):
		self.state_index = (self.state_index + 1) % len(self.states)
		self.foreground.text = self.state_names[self.state_index]
		if self.callback is not None:
			self.callback(self, self.states[self.state_names[self.state_index]])

	def do_claim(self):
		max_x, max_y = 0, 0
		for text in self.state_names:
			test_label = self.Foreground(text)
			text_width, text_height = test_label.do_claim()
			max_x, max_y = max(max_x, text_width), max(max_y, text_height)
		return max_x, max_y
	
	class Base(glooey.Background):
		custom_color = '#aa1e1eff'

	class Over(glooey.Background):
		custom_color = '#cc3f3fdd'

	class Down(glooey.Background):
		custom_color = '#ff5d5daa'


class SmallCycleButton(CycleButton):
	Foreground = Description