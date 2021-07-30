import pyglet
import glooey
from .labels import ButtonLabel


class Button(glooey.Button):
	Foreground = ButtonLabel
	custom_alignment = 'fill'

	def __init__(self, *args, action=None, action_params=[], **kwargs):
		super().__init__(*args, **kwargs)
		self.action = action
		self.action_params = action_params

	def on_click(self, widget):
		if self.action:
			self.action(*self.action_params)

	class Base(glooey.Background):
		custom_color = '#aa1e1e'

	class Over(glooey.Background):
		custom_color = '#cc3f3f'

	class Down(glooey.Background):
		custom_color = '#ff5d5d'


class CycleButton(glooey.Button):
	Foreground = ButtonLabel
	custom_alignment = 'fill'

	def __init__(self, states, state_change_callback=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.states = states
		self.state_keys = list(self.states.keys())
		self.state_index = 0
		self.state_change_callback = state_change_callback
		self.foreground.text = self.states[self.state_keys[self.state_index]]

	def on_click(self, widget):
		self.state_index = (self.state_index + 1) % len(self.states)
		self.foreground.text = self.states[self.state_keys[self.state_index]]
		if self.state_change_callback is not None:
			self.state_change_callback(self.state_keys[self.state_index])
	
	class Base(glooey.Background):
		custom_color = '#aa1e1eff'

	class Over(glooey.Background):
		custom_color = '#cc3f3fdd'

	class Down(glooey.Background):
		custom_color = '#ff5d5daa'
