import pyglet
import numpy as np
from .starobject import StarObject
from ..utils import create_sprite
from ..scenes.groups.parallax import ParallaxGroup
from ..globals import WINDOW_WIDTH, WINDOW_HEIGHT


class BackgroundObject:

	def __init__(self, background_image, batch, group, random_seed=0, n_stars=100, n_layers=3):
		
		self.batch = batch
		self.group = group
		self.sprite = create_sprite(
			background_image,
			anchor='bottom_left',
			size=(WINDOW_WIDTH, WINDOW_HEIGHT),
			batch=batch, 
			group=group
		)

		scale_x, scale_y = WINDOW_WIDTH / self.sprite.width, WINDOW_HEIGHT / self.sprite.height
		self.sprite.update(scale_x=scale_x, scale_y=scale_y)
		self.sprite.opacity = 180

		np.random.seed(random_seed)

		self.n_stars = n_stars
		self.n_layers = n_layers
		self.layers = [ParallaxGroup(20 + 5*n, n) for n in range(self.n_layers)]

		# MESS
		self.old_width = WINDOW_WIDTH
		self.old_height = WINDOW_HEIGHT

		self.populate_stars()

	def populate_stars(self):
		self.stars = []
		stars_img = [
			'assets/sprites/particle_star1_1.png',
			'assets/sprites/particle_star1_2.png',
			'assets/sprites/particle_star2_1.png',
			'assets/sprites/particle_star2_2.png'
		]
		for i in range(self.n_stars):
			self.stars.append(
				StarObject(
					pos=np.random.rand(2)*np.array((WINDOW_WIDTH, WINDOW_HEIGHT)),
					sprite=create_sprite(
						np.random.choice(stars_img),
						size=(5, 5),
						batch=self.batch,
						group=np.random.choice(self.layers)
					)
				)
			)

	def reset(self):
		# I attempted to fix the background not moving issue on reset, did not work...
		for i in range(self.n_stars-1, 0, -1):
			self.stars[i].sprite.delete()
			self.stars.pop(i)
		self.sprite.delete()

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		for layer in self.layers:
			layer.offset += (dx, dy)

	def on_resize(self, width, height):
		scale_x, scale_y = width / WINDOW_WIDTH, height / WINDOW_HEIGHT
		self.sprite.update(scale_x=scale_x, scale_y=scale_y)
		# Inexpensive resize
		# for layer in self.layers:
		# 	layer.scale_x = width / WINDOW_WIDTH
		# 	layer.scale_y = height / WINDOW_HEIGHT

		# Expensive resize
		for star in self.stars:
			star.sprite.x *= width / self.old_width
			star.sprite.y *= height / self.old_height

		self.old_width, self.old_height = width, height
