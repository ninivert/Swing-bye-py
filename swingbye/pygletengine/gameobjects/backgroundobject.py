import pyglet
import numpy as np
from .starobject import StarObject
from ..utils import create_sprite
from ..scenes.layers.parallax import ParallaxGroup
import swingbye.pygletengine.globals as g


class BackgroundObject:

	def __init__(self, background_image, camera, batch, group, random_seed=0, n_stars=100, n_layers=3, layers=[]):
		
		self.camera = camera
		self.batch = batch
		self.group = group

		np.random.seed(random_seed)

		self.sprite = create_sprite(
			background_image,
			anchor='bottom_left',
			size=(g.WINDOW_WIDTH, g.WINDOW_HEIGHT),
			batch=batch, 
			group=group
		)
		self.sprite.opacity = 180

		self.n_stars = n_stars
		self.n_layers = n_layers

		self.layers = layers
		# for i in range(n_layers):
		# 	self.layers.append(ParallaxGroup(i, rate=1/(i+6)**2))

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
					pos=np.random.rand(2)*np.array((g.WINDOW_WIDTH, g.WINDOW_HEIGHT)),
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
		for i in self.stars:
			i.delete()
		self.stars.empty()

	def update(self):
		for layer in self.layers:
			layer.offset = self.camera.offset + self.camera.anchor

	def on_resize(self, width, height):
		scale_x, scale_y = width / g.WINDOW_WIDTH, height / g.WINDOW_HEIGHT
		self.sprite.update(scale_x=scale_x, scale_y=scale_y)
		print(scale_x, scale_y)
