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

		self.old_width, self.old_height = WINDOW_WIDTH, WINDOW_HEIGHT

		# self.populate_stars()

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

	def delete(self):
		self.sprite.delete()

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		pass

	def on_resize(self, width, height):
		scale_x, scale_y = width / self.old_width, height / self.old_height
		self.sprite.update(scale_x=scale_x, scale_y=scale_y)
		self.old_width, self.old_height = width, height
