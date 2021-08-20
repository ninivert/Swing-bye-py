import pyglet
import glooey
from .labels import ButtonLabel


class Button(glooey.Button):
	Foreground = ButtonLabel
	custom_alignment = 'fill'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def on_click(self, widget):
		self.dispatch_event('on_press')

	class Base(glooey.Background):
		custom_color = '#aa1e1e'

	class Over(glooey.Background):
		custom_color = '#cc3f3f'

	class Down(glooey.Background):
		custom_color = '#ff5d5d'


Button.register_event_type('on_press')


class CycleButton(glooey.Button):
	Foreground = ButtonLabel
	custom_alignment = 'fill'

	def __init__(self, states, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.states = states
		self.state_keys = list(self.states.keys())
		self.state_index = 0
		self.foreground.text = self.states[self.state_keys[self.state_index]]

	def on_click(self, widget):
		self.state_index = (self.state_index + 1) % len(self.states)
		self.foreground.text = self.states[self.state_keys[self.state_index]]
		self.dispatch_event('on_toggle', self.state_keys[self.state_index])

	def do_claim(self):
		max_x, max_y = 0, 0
		for text in self.states.values():
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


CycleButton.register_event_type('on_toggle')
