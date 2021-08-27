import pyglet
import glooey
from swingbye.pygletengine.utils import point_in_rect
from swingbye.pygletengine.components.slider import Slider
from swingbye.pygletengine.components.graph import LineGraph
from swingbye.pygletengine.components.overlays import GraphOverlay
from swingbye.pygletengine.components.labels import Title, Subtitle
from swingbye.pygletengine.components.buttons import Button, CycleButton
from swingbye.pygletengine.components.containers import VBox, HBox, Board, Frame, Dialog
from swingbye.pygletengine.globals import GameState


class PauseOverlay(Frame):
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


class WinOverlay(Frame):
	Background = glooey.images.Background
	custom_alignment = 'center'

	def __init__(self):
		super().__init__()

		self.decoration.color = (255, 20, 25)

		self.container = VBox()

		self.title = Title('You win!')
		self.subtitle = Subtitle('click to continue')
		
		self.container.add(self.title)
		self.container.add(self.subtitle)
		
		self.add(self.container)


class LoseOverlay(Frame):
	Background = glooey.images.Background
	custom_alignment = 'center'

	def __init__(self):
		super().__init__()

		self.decoration.color = (255, 20, 25)

		self.container = VBox()

		self.title = Title('You lose...')
		self.subtitle = Subtitle('click to continue')
		
		self.container.add(self.title)
		self.container.add(self.subtitle)
		
		self.add(self.container)


class HudObject:

	def __init__(self, gui):

		self.gui = gui
		self.captured = False

		self.container = Board()
		self.hud_container = glooey.HBox()

		# Overlays
		self.overlays = {}
		graph = GraphOverlay(
			LineGraph(
				100, 100,
				lines=[
					{
						'name': 'KE',
						'path': None,
						'query': None,
						'color': (255, 128, 69, 255),
						'samples': [],
						'size': 100,
					},
					{
						'name': 'PE',
						'path': None,
						'query': None,
						'color': (69, 83, 255, 255),
						'samples': [],
						'size': 100,
					},
					{
						'name': 'TOTAL',
						'path': None,
						'query': None,
						'color': (0, 0, 0, 255),
						'samples': [],
						'size': 100,
					}
				],
				y_scale_mode='auto'
			)
		)
		pause = PauseOverlay()
		win = WinOverlay()
		lose = LoseOverlay()
		self.add_overlay('graph', graph)
		self.add_overlay('pause', pause)
		self.add_overlay('win', win)
		self.add_overlay('lose', lose)

		# Bottom control buttons
		self.reset_button = Button('Reset')
		self.pause_button = Button('Pause')
		self.speed_slider = Slider(
			min_value=1, max_value=16,
			step=1,
			edge=10,
			min_width=100
		)
		self.time_slider = Slider(
			min_value=0, max_value=50000,
			step=25,
			edge=10,
			min_width=100
		)
		self.launch_button = Button('LAUNCH')

		# Attach everything to their containers
		self.hud_container.pack(self.reset_button)
		self.hud_container.pack(self.pause_button)
		self.hud_container.pack(self.speed_slider)
		self.hud_container.add(self.time_slider)
		self.hud_container.pack(self.launch_button)

		self.container.add(self.hud_container, left=0, bottom=0, width_percent=1)
		self.open_overlay('graph', left=10, bottom=50)

		self.gui.add(self.container)

	def is_over(self, x, y):
		over = False
		for child, _ in self.container._pins.items():
			over = over or point_in_rect(x, y, *child.rect.bottom_left, child.width, child.height)
		return over

	def add_overlay(self, name, overlay):
		self.overlays[name] = overlay

	def open_overlay(self, name, *args, **kwargs):
		self.container.add(self.overlays[name], *args, **kwargs)

	def close_overlay(self, name):
		self.container.remove(self.overlays[name])

	def hide_graph(self):
		self.overlays['graph'].hide()

	def show_graph(self):
		self.overlays['graph'].unhide()

	def reset(self):
		self.overlays['graph'].graph.reset()
		self.time_slider.reset()

	def on_mouse_press(self, x, y, buttons, modifiers):
		self.captured = True
		# TODO: close overlays correctly
		# if point_in_rect(x, y, *self.overlays['win'].rect.bottom_left, self.overlays['win'].width, self.overlays['win'].height):
		# 	self.close_overlay('win')
		# if point_in_rect(x, y, *self.overlays['lose'].rect.bottom_left, self.overlays['lose'].width, self.overlays['lose'].height):
		# 	self.close_overlay('lose')

	def on_mouse_release(self, x, y, buttons, modifiers):
		self.time_slider.on_mouse_release(x, y, buttons, modifiers)
		self.speed_slider.on_mouse_release(x, y, buttons, modifiers)
		self.captured = False

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.time_slider.captured:
			self.time_slider.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
		if self.speed_slider.captured:
			self.speed_slider.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

	def on_win(self):
		self.overlays['graph'].graph.pause_sampling()
		self.open_overlay('win', center_percent=(0.5, 0.5))

	def on_lose(self):
		self.overlays['graph'].graph.pause_sampling()
		self.open_overlay('lose', center_percent=(0.5, 0.5))

	def on_pause(self):
		self.overlays['graph'].graph.pause_sampling()
		self.open_overlay('pause', center_percent=(0.5, 0.5))

	def on_resume(self):
		self.close_overlay('pause')
		self.overlays['graph'].graph.pause_sampling()

