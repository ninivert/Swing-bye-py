import pyglet
from pyglet.window import key
import glooey
from .globals import WINDOW_WIDTH, WINDOW_HEIGHT
from .mainmenu import MainMenu
from .level import Level
from .levelselectmenu import LevelSelectMenu
from .optionsmenu import OptionsMenu


class ViewController(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, *args, **kwargs)

		self.batch = pyglet.graphics.Batch()
		self.frame_rate = 1/60.0
		self.game_loop = None

		self.keys = key.KeyStateHandler()
		self.push_handlers(self.keys)
		self.fps_display = pyglet.window.FPSDisplay(self)

		self.gui = glooey.Gui(self, batch=self.batch)

		self.views = {
			'MainMenu': MainMenu(self),
			'Level': Level(self),
			'LevelSelectMenu': LevelSelectMenu(self),
			'OptionsMenu': OptionsMenu(self)
		}

		self.views['MainMenu'].begin()


	def on_key_press(self, symbol, modifier):
		if symbol == key.ESCAPE:
			pyglet.app.exit()

	def on_draw(self):
		self.clear()
		self.batch.draw()
		self.fps_display.draw()

	def update(self, dt):
		if self.game_loop:
			self.game_loop(dt)
