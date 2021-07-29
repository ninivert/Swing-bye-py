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

		### TEMPORTARY TESTING
		self.mouse_x = 0
		self.mouse_y = 0
		self.dx = 0
		self.dy = 0
		self.zoom_factor = 1
		self.pause = False
		###

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

		self.views['Level'].begin()

	def on_key_press(self, symbol, modifier):
		if symbol == key.ESCAPE:
			pyglet.app.exit()
		if symbol == key.F4 and modifier & key.MOD_ALT:
			pyglet.app.exit()
		if symbol == key.SPACE:
			self.pause = not self.pause
		if symbol == key._0:
			self.views['Level'].camera.reset()

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_motion(self, x, y, dx, dy):
		self.mouse_x = x
		self.mouse_y = y

	def on_draw(self):
		self.clear()
		self.batch.draw()
		self.fps_display.draw()

	def update(self, dt):
		if self.game_loop and not self.pause:
			self.game_loop(dt)
