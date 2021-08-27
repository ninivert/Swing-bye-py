import pyglet
import numpy as np
import json
import logging
from swingbye.levels.parser import parse_level
from swingbye.physics.world import WorldStates
from swingbye.pygletengine.utils import point_in_rect
from swingbye.pygletengine.scenes.scene import Scene
from swingbye.pygletengine.scenes.layers.camera import Camera
from swingbye.pygletengine.gameobjects.backgroundobject import BackgroundObject
from swingbye.pygletengine.gameobjects.hudobject import HudObject
from swingbye.pygletengine.globals import WINDOW_WIDTH, WINDOW_HEIGHT, DEBUG_CAMERA, DEBUG_COLLISION, TEST_COLLISIONS, GameState, GameEntity
from swingbye.globals import PHYSICS_DT

_logger = logging.getLogger(__name__)

class Level(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.register_event_type('on_win')
		self.register_event_type('on_lose')
		self.register_event_type('on_reset')

		self.levels = ['swingbye/levels/level1.json']
		self.level_index = 0

		# TODO : cleanup this
		self.mouse_press_x = 0
		self.mouse_press_y = 0

		self.simulation_speed = 1
		self.game_state = GameState.RUNNING

		self.mouse_x = 0
		self.mouse_y = 0

	def on_mouse_motion(self, x, y, dx, dy):
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.game_state == GameState.RUNNING:
			if self.hud.captured:
				pass
			else:
				self.camera.move(-dx, -dy)
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_press(self, x, y, buttons, modifiers):
		self.mouse_press_x = x
		self.mouse_press_y = y
		if self.hud.is_over(x, y):
			self.hud.on_mouse_press(x, y, buttons, modifiers)

	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.game_state == GameState.RUNNING:
			clicked = self.mouse_press_x == x and self.mouse_press_y == y
			if not self.hud.is_over(x, y):
				if clicked:
					self.world.point_ship(self.camera.screen_to_world(x, y))

		self.hud.on_mouse_release(x, y, buttons, modifiers)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if self.game_state == GameState.RUNNING:
			if not self.hud.is_over(x, y):
				if scroll_y != 0:
					self.camera.zoom_at(x, y, scroll_y)

	def on_resize(self, width, height):
		self.background.on_resize(width, height)
		self.camera.on_resize(width, height)

	def on_speed_change(self, widget, value):
		self.simulation_speed = int(value)
		self.hud.overlays['graph'].graph.sample_rate = 1/10 / int(value)

	def on_time_change(self, widget, value):
		self.world.time = value

	def on_pause(self):
		self.game_state = GameState.PAUSED
		self.hud.on_pause()

	def on_resume(self):
		self.game_state = GameState.RUNNING
		self.hud.on_resume()

	def on_win(self):
		self.game_state = GameState.ENDING
		self.hud.on_win()

	def on_lose(self):
		self.game_state = GameState.ENDING
		self.hud.on_lose()

	def on_reset(self):
		self.reset()

	def load_hud(self):
		self.hud = HudObject(self.gui)

		self.hud.overlays['control'].reset_button.callback = self.reset
		self.hud.overlays['control'].pause_button.callback = self.on_pause
		self.hud.overlays['control'].speed_slider.callback =  self.on_speed_change
		self.hud.overlays['control'].time_slider.callback =  self.on_time_change
		self.hud.overlays['control'].launch_button.callback = self.launch_ship

		self.hud.overlays['pause'].resume_button.callback = self.on_resume
		self.hud.overlays['pause'].quit_button.callback = pyglet.app.exit

		self.hud.overlays['graph'].graph.set_query('KE', self.world.kinetic_energy)
		self.hud.overlays['graph'].graph.set_query('PE', self.world.potential_energy)
		self.hud.overlays['graph'].graph.set_query('TOTAL', lambda: self.world.potential_energy() + self.world.kinetic_energy())
		self.hud.hide_graph()

		self.entity_label = pyglet.text.Label('AAAAAAA', batch=self.world_batch, group=pyglet.graphics.OrderedGroup(1, parent=self.world_group))

	def load_level(self):
		with open(self.levels[self.level_index]) as file:
			level = json.load(file)

		self.background = BackgroundObject(
			level['background_sprite'],
			self.camera,
			self.batch,
			self.background_group
		)

		_logger.debug(f'parsing level from file `{self.levels[self.level_index]}`')

		self.world = parse_level(level, self.world_batch, self.world_group)

	def load(self):
		self.batch = pyglet.graphics.Batch()
		self.world_batch = pyglet.graphics.Batch()

		self.background_group = pyglet.graphics.OrderedGroup(0)
		self.world_group = pyglet.graphics.OrderedGroup(1)
		self.foreground_group = pyglet.graphics.OrderedGroup(2)

		self.camera = Camera(self.window)

		if DEBUG_CAMERA:
			self.offset_line = pyglet.shapes.Line(0, 0, 0, 0, color=(255, 20, 20), batch=self.batch, group=self.foreground_group)
			self.mouse_line = pyglet.shapes.Line(0, 0, 0, 0, color=(20, 255, 20), batch=self.world_batch, group=self.foreground_group)
			self.mouse_world_to_screen_line = pyglet.shapes.Line(0, 0, 0, 0, color=(255, 255, 20), batch=self.batch, group=self.foreground_group)

		self.load_level()
		self.load_hud()

		self.camera.set_parent(self.world.ship)

	def begin(self):
		self.gui.clear()
		self.load()

	def draw(self):
		self.batch.draw()
		with self.camera:
			self.world_batch.draw()
			if DEBUG_COLLISION:
				for planet in self.world.planets:
					pyglet.shapes.Circle(*planet.pos, planet.radius).draw()
				pyglet.shapes.Circle(*self.world.ship.pos, self.world.ship.radius).draw()
		self.gui.batch.draw()

	def run(self, dt):
		# TODO: find a way to update the camera here instead of before drawing (make it independent of fps)
		# self.camera.update()
		# TODO: fix stars jumping around when changing zoom anchor
		# self.background.update()

		if self.game_state == GameState.RUNNING:
			if self.world.state == WorldStates.POST_LAUNCH:
				for i in range(self.simulation_speed):
					self.world.step(PHYSICS_DT)

					if TEST_COLLISIONS:
						self.check_collision()

		if DEBUG_CAMERA:
			# WARNING: lines are always late by 1 frame
			# do not trust them too much on fast moving entities
			self.offset_line.x2, self.offset_line.y2 = self.camera.world_to_screen(*self.world.planets[0].pos)
			self.mouse_line.x2, self.mouse_line.y2 = self.camera.screen_to_world(self.mouse_x, self.mouse_y)
			self.mouse_world_to_screen_line.x2, self.mouse_world_to_screen_line.y2 = self.camera.world_to_screen(*self.camera.screen_to_world(self.mouse_x, self.mouse_y))

	# Game logic

	def launch_ship(self):
		self.world.launch_ship()
		self.hud.show_graph()

	def check_collision(self):
		for planet in self.world.planets:
			if self.world.ship.collides_with(planet):
				if planet.game_entity == GameEntity.PLANET:
					self.dispatch_event('on_lose')
				elif planet.game_entity == GameEntity.WORMHOLE:
					self.dispatch_event('on_win')

	def reset(self):
		self.hud.reset()
		self.hud.hide_graph()
		self.camera.set_parent(None)

		# This is very bad, old objects are not getting cleaned up (sprites need to be removed from batches etc)
		# When reset is spammed, memory usage increases greatly
		# TODO -= 1  # yay
		self.load_level()
		self.camera.set_parent(self.world.ship)
