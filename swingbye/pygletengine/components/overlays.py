import pyglet
import glooey
from swingbye.pygletengine.components.slider import Slider
from swingbye.pygletengine.components.buttons import Button, SmallCycleButton, SmallButton
from swingbye.pygletengine.components.labels import Description, Subtitle
from swingbye.pygletengine.components.containers import Frame, HBox, VBox


class Overlay(Frame):
	custom_alignment = 'center'


class GraphOverlay(Overlay):

	def __init__(self, graph):
		super().__init__()

		self.graph = graph
		self.add(self.graph)


class OptionsOverlay(Overlay):
	Background = glooey.images.Background
	custom_alignment = 'center'

	def __init__(self, title, options_dict):
		super().__init__()

		self.register_event_type('on_option_change')

		self.vbox = VBox()

		self.title = Subtitle(title)
		self.vbox.pack(self.title)

		self.widget_nametable = {}
		self.option_values = {}

		self.construct_menu(options_dict)

		# self.cancel_button = Button('Cancel')
		# self.confirm_button = Button('Confirm')
		# self.cancel_button.set_handler('on_press', self.on_press)
		# self.confirm_button.set_handler('on_press', self.on_press)

		# hbox = HBox()
		# hbox.add(self.cancel_button)
		# hbox.add(self.confirm_button)
		# self.vbox.pack(hbox)

		self.add(self.vbox)

	def construct_menu(self, options_dict):
		for name in options_dict.keys():

			# Personal container for option
			# Name
			# Value modifier
			if options_dict[name]['type'] == 'slider':
				self.add_row_slider(name, options_dict[name])
			if options_dict[name]['type'] == 'cycle':
				self.add_row_cycle(name, options_dict[name])
			if options_dict[name]['type'] == 'button':
				self.add_row_single_button(name, options_dict[name])

	def add_row_slider(self, name, options_dict):
		description = Description(options_dict['description'])
		widget = Slider(
			value=options_dict['default'],
			min_value=options_dict['min_value'],
			max_value=options_dict['max_value'],
			step=options_dict['step'],
			edge=10,
			min_width=100
		)
		widget.set_handler('on_change', self.on_change)

		# Add row to menu
		row = HBox()
		row.pack(description)
		row.add(widget)
		self.vbox.pack(row)

		# Keep track of what widget does what and values
		self.option_values[name] = options_dict['default']
		self.widget_nametable[widget] = name

	def add_row_cycle(self, name, options_dict):
		description = Description(options_dict['description'])
		widget = SmallCycleButton(options_dict['states'], default=options_dict['default'])
		widget.set_handler('on_change', self.on_change)

		# Add row to menu
		row = HBox()
		row.pack(description)
		row.add(widget)
		self.vbox.pack(row)

		# Keep track of what widget does what and values
		self.option_values[name] = options_dict['default']
		self.widget_nametable[widget] = name

	def add_row_single_button(self, name, options_dict):
		widget = SmallButton(options_dict['label'], options_dict['callback'])

		row = HBox()
		row.add(widget)
		self.vbox.pack(row)

	def on_change(self, widget, value):
		self.option_values[self.widget_nametable[widget]] = value
		self.dispatch_event('on_option_change', self.widget_nametable[widget], value)
