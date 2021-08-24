import pyglet
from pyglet.window import key
import glooey
from swingbye.pygletengine.scenes.mainmenu import MainMenu
from swingbye.pygletengine.scenes.level import Level
from swingbye.pygletengine.scenes.levelselectmenu import LevelSelectMenu
from swingbye.pygletengine.scenes.optionsmenu import OptionsMenu
from swingbye.pygletengine.scenes.dvd import DVD
from swingbye.pygletengine.scenes.testing import Test
import swingbye.pygletengine.globals as g


class ViewController(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super().__init__(g.WINDOW_WIDTH, g.WINDOW_HEIGHT, *args, **kwargs)

		self.gui_batch = pyglet.graphics.Batch()
		self.gui_group = pyglet.graphics.Group()
		self.frame_rate = 1/60.0

		if g.DEBUG_PERF:
			self.fps_display = pyglet.window.FPSDisplay(self)
			self.fps_display.label.x, self.fps_display.label.y = 0, g.WINDOW_HEIGHT-50

		self.gui = glooey.Gui(self, batch=self.gui_batch, group=self.gui_group)

		self.scenes = {
			'MainMenu': MainMenu(self, self.gui, self.transition_to_scene),
			'Level': Level(self, self.gui, self.transition_to_scene),
			'LevelSelectMenu': LevelSelectMenu(self, self.gui, self.transition_to_scene),
			'OptionsMenu': OptionsMenu(self, self.gui, self.transition_to_scene),
			'DVD': DVD(self, self.gui, self.transition_to_scene),
			'Test': Test(self, self.gui, self.transition_to_scene)
		}

		self.push_handlers()

		self.current_scene = 'MainMenu'
		self.transition_to_scene('MainMenu')

	def transition_to_scene(self, scene: str):
		self.remove_handlers(self.scenes[self.current_scene])
		self.current_scene = scene
		self.scenes[self.current_scene].begin()
		self.push_handlers(self.scenes[self.current_scene])

	def on_key_press(self, symbol, modifier):
		if symbol == key.ESCAPE:
			if self.current_scene == 'MainMenu':
				pyglet.app.exit()
			self.transition_to_scene('MainMenu')
		if symbol == key.F4 and modifier & key.MOD_ALT:
			pyglet.app.exit()

		# For testing only
		if symbol == key._0:
			self.scenes['Level'].camera.set_parent(None)
		if symbol == key._1:
			self.scenes['Level'].camera.set_parent(self.scenes['Level'].world.planets[0])
		if symbol == key._2:
			self.scenes['Level'].camera.set_parent(self.scenes['Level'].world.ship)

	def on_draw(self):
		self.clear()
		self.scenes[self.current_scene].draw()
		if g.DEBUG_PERF:
			self.fps_display.draw()

	def on_resize(self, width, height):
		super().on_resize(width, height)
		g.WINDOW_WIDTH = width
		g.WINDOW_HEIGHT = height

	def update(self, dt):
		self.scenes[self.current_scene].run(dt)
