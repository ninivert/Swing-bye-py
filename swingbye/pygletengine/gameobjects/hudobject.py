import pyglet
import glooey
from swingbye.pygletengine.components.slider import Slider
from swingbye.pygletengine.components.graph import Graph
from swingbye.pygletengine.components.labels import Title
from swingbye.pygletengine.components.buttons import Button, CycleButton
from swingbye.pygletengine.components.containers import VBox, HBox, Board, Frame, Dialog
from swingbye.pygletengine.globals import GameState


class PauseMenu(Dialog):
	Background = glooey.images.Background

	def __init__(self):
		super().__init__()

		self.container = VBox()

		self.title = Title('Pause Menu')
		self.resume_button = Button('Resume')
		self.quit_button = Button('Quit')

		self.container.add(self.title)
		self.container.add(self.resume_button)
		self.container.add(self.quit_button)

		self.add(self.container)


class HudObject:

	def __init__(self, gui):

		self.container = glooey.VBox()
		self.hud_container = glooey.HBox()
		self.graph_container = Frame()
		self.overlay = Board()

		# Graph overlay
		self.graph = Graph(
			100, 100,
			y_scale_mode='fixed_min',
			min_y=0
		)

		# Bottom control buttons
		self.reset_button = Button('Reset')
		self.pause_button = Button('Pause')
		self.speed_slider = Slider(
			min_value=1, max_value=16,
			step=1,
			edge=10
		)
		self.time_slider = Slider(
			min_value=0, max_value=50000,
			step=25,
			edge=10
		)
		self.launch_button = Button('LAUNCH')

		self.pause_menu = PauseMenu()
		
		# Attach everything to their containers
		self.graph_container.add(self.graph)
		self.overlay.add(self.graph_container, left=10, bottom=10)

		self.hud_container.pack(self.reset_button)
		self.hud_container.pack(self.pause_button)
		self.hud_container.pack(self.speed_slider)
		self.hud_container.add(self.time_slider)
		self.hud_container.pack(self.launch_button)

		self.container.add(self.overlay)
		self.container.pack(self.hud_container)


		gui.add(self.container)

	@property
	def rect(self):
		"""Return the bounding rect of the control buttons"""
		return self.hud_container.rect

	@property
	def captured(self):
		return self.speed_slider.captured or self.time_slider.captured

	def hide_graph(self):
		self.graph_container.hide()

	def show_graph(self):
		self.graph_container.unhide()

	def reset(self):
		self.graph.reset()
		self.time_slider.reset()

	def on_mouse_press(self, x, y, buttons, modifiers):
		pass

	def on_mouse_release(self, x, y, buttons, modifiers):
		self.time_slider.on_mouse_release(x, y, buttons, modifiers)
		self.speed_slider.on_mouse_release(x, y, buttons, modifiers)

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.time_slider.captured:
			self.time_slider.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
		if self.speed_slider.captured:
			self.speed_slider.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
