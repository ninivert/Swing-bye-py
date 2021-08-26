import pyglet
import glooey
from swingbye.pygletengine.components.slider import Slider
from swingbye.pygletengine.components.buttons import Button
from swingbye.pygletengine.components.labels import Description
from swingbye.pygletengine.components.containers import Frame, HBox, VBox


class Options(Frame):
	Background = glooey.images.Background
	custom_alignment = 'center'

	def __init__(self, options_dict):
		super().__init__()

		self.register_event_type('on_option_change')
		self.register_event_type('on_confirm')

		self.vbox = VBox()

		self.widget_nametable = {}
		self.option_values = {}

		self.construct_menu(options_dict)

		self.confirm_button = Button('Confirm')
		self.confirm_button.set_handler('on_press', self.on_confirm_press)
		self.vbox.pack(self.confirm_button)

		self.add(self.vbox)

	def construct_menu(self, options_dict):
		for name in options_dict.keys():

			# Personal container for option
			container = HBox()
			# Name
			description = Description(name)
			# Value modifier
			if options_dict[name]['type'] == 'slider':
				widget = Slider(
					value=options_dict[name]['default'],
					min_value=options_dict[name]['min_value'],
					max_value=options_dict[name]['max_value'],
					step=options_dict[name]['step'],
					edge=10,
					min_width=100
				)
				widget.set_handler('on_change', self.on_change)
				self.option_values[name] = options_dict[name]['default']
			# Keep track of what widget does what
			self.widget_nametable[widget] = name

			# Add option to menu
			container.pack(description)
			container.add(widget)
			self.vbox.pack(container)

	def on_change(self, widget, value):
		self.option_values[self.widget_nametable[widget]] = value
		self.dispatch_event('on_option_change', self.widget_nametable[widget], value)

	def on_confirm_press(self):
		self.dispatch_event('on_confirm', self.option_values)

