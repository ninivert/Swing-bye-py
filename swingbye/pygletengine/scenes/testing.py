import pyglet
import glooey
from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.components.containers import Freeform, Board
from swingbye.pygletengine.components.overlays import Options
from swingbye.pygletengine.globals import WINDOW_WIDTH, WINDOW_HEIGHT


# Testing environment for testing new custom widgets and stuff


class Test(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.container = Board()

		options = {
			'option111111': {
				'type': 'slider',
				'default': 0,
				'min_value': 0,
				'max_value': 100,
				'step': 1
			},
			'option2': {
				'type': 'slider',
				'default': 420,
				'min_value': 69,
				'max_value': 420,
				'step': 1
			},
			'option3': {
				'type': 'slider',
				'default': 10,
				'min_value': -1,
				'max_value': 20,
				'step': 1
			}
		}
		self.options_overlay = Options(options)
		self.options_overlay.set_handler('on_option_change', self.on_option_change)
		self.options_overlay.set_handler('on_confirm', self.on_confirm)

		self.container.add(self.options_overlay, bottom_left=(10, 10))

	def on_option_change(self, name, value):
		print(name, value)

	def on_confirm(self, options):
		print(options)

	def begin(self):
		
		self.gui.clear()

		self.load()

		self.gui.add(self.container)
		# self.container.debug_placement_problems()
	
	def draw(self):
		self.gui.batch.draw()
