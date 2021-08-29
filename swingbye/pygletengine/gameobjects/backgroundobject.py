import pyglet
import numpy as np
from swingbye.pygletengine.gameobjects.entities import StarObject
from swingbye.pygletengine.utils import create_sprite
from swingbye.pygletengine.scenes.layers.parallax import ParallaxGroup
import swingbye.pygletengine.globals as g


class BackgroundObject:

	def __init__(self, background_image, camera, batch, group, random_seed=0, n_stars=100, layers=[]):
		self.camera = camera
		self.batch = batch
		self.group = group

		np.random.seed(random_seed)

		self.old_width = g.WINDOW_WIDTH
		self.old_height = g.WINDOW_HEIGHT

		self.n_stars = n_stars

		self.sprite = create_sprite(
			background_image,
			anchor='bottom_left',
			size=(g.WINDOW_WIDTH, g.WINDOW_HEIGHT),
			batch=batch,
			group=pyglet.graphics.OrderedGroup(1, parent=self.group)
		)
		self.sprite.opacity = 180

		self.stars_group = ParallaxGroup(0, rate=1/50, parent=self.group)
	
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
					pos=np.random.rand(2)*np.array((self.sprite.width, self.sprite.height)),
					sprite=create_sprite(
						np.random.choice(stars_img),
						size=(5, 5),
						batch=self.batch,
						group=self.stars_group
					)
				)
			)

	def delete(self):
		self.sprite.delete()
		for i in self.stars:
			i.delete()
		self.stars.clear()

	# def update(self):
	# 	for layer in self.layers:
	# 		layer.offset = self.camera.offset + self.camera.anchor

	def on_resize(self, width, height):
		# FIXME: do not hardcode
		scale_x, scale_y = width / 1280, height / 720
		self.sprite.update(scale_x=scale_x, scale_y=scale_y)

		for star in self.stars:
			star.sprite.x *= width / self.old_width
			star.sprite.y *= height / self.old_height

		self.old_width, self.old_height = width, height
