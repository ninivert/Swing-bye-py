import pyglet
from pyglet.window import key
import glooey
from .scenes.mainmenu import MainMenu
from .scenes.level import Level
from .scenes.levelselectmenu import LevelSelectMenu
from .scenes.optionsmenu import OptionsMenu
from .scenes.dvd import DVD
from .scenes.testing import Test
from .globals import WINDOW_WIDTH, WINDOW_HEIGHT, DEBUG


class ViewController(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, *args, **kwargs)

		self.gui_batch = pyglet.graphics.Batch()
		self.frame_rate = 1/60.0

		if DEBUG:
			self.fps_display = pyglet.window.FPSDisplay(self)
			self.fps_display.label.x, self.fps_display.label.y = 0, WINDOW_HEIGHT-50

		self.gui = glooey.Gui(self, batch=self.gui_batch)

		self.scenes = {
			'MainMenu': MainMenu(self, self.gui, self.transition_to_scene),
			'Level': Level(self, self.gui, self.transition_to_scene),
			'LevelSelectMenu': LevelSelectMenu(self, self.gui, self.transition_to_scene),
			'OptionsMenu': OptionsMenu(self, self.gui, self.transition_to_scene),
			'DVD': DVD(self, self.gui, self.transition_to_scene),
			'Test': Test(self, self.gui, self.transition_to_scene)
		}

		self.push_handlers()

		self.transition_to_scene('MainMenu')

	def transition_to_scene(self, scene: str):
		self.current_scene = scene
		self.pop_handlers()
		self.push_handlers(self.scenes[self.current_scene])
		self.scenes[self.current_scene].begin()

	def on_key_press(self, symbol, modifier):
		if symbol == key.ESCAPE:
			if self.current_scene == 'MainMenu':
				pyglet.app.exit()
			self.transition_to_scene('MainMenu')
		if symbol == key.F4 and modifier & key.MOD_ALT:
			pyglet.app.exit()

		# For testing only
		if symbol == key._0:
			self.scenes['Level'].camera.set_parent(self.scenes['Level'].world.planets[0])
		if symbol == key._1:
			self.scenes['Level'].camera.set_parent(self.scenes['Level'].world.ship)

	def on_draw(self):
		self.clear()
		self.scenes[self.current_scene].draw()
		if DEBUG:
			self.fps_display.draw()

	def update(self, dt):
		self.scenes[self.current_scene].run(dt)
