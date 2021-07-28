import pyglet


def center_anchor(image):
	image.anchor_x = image.width // 2
	image.anchor_y = image.height // 2
	return image


images = {
	'planet1': center_anchor(pyglet.ressource.image('assets/sprites/planet1.png')),
	'planet2': center_anchor(pyglet.resource.image('assets/sprites/planet2.png')),
	'planet3': center_anchor(pyglet.resource.image('assets/sprites/planet3.png')),
	'planet4': center_anchor(pyglet.resource.image('assets/sprites/planet4.png')),
	'planet5': center_anchor(pyglet.resource.image('assets/sprites/planet5.png')),
	'star1': center_anchor(pyglet.resource.image('assets/sprites/star1.png')),
	'star2': center_anchor(pyglet.resource.image('assets/sprites/star2.png')),
	'star3': center_anchor(pyglet.resource.image('assets/sprites/star3.png')),
	'particle_star1_1': center_anchor(pyglet.resource.image('assets/sprites/particle_star1_1.png')),
	'particle_star1_2': center_anchor(pyglet.resource.image('assets/sprites/particle_star1_2.png')),
	'particle_star2_1': center_anchor(pyglet.resource.image('assets/sprites/particle_star2_1.png')),
	'particle_star2_2': center_anchor(pyglet.resource.image('assets/sprites/particle_star2_2.png')),
	'ship_on': center_anchor(pyglet.ressource.image('assets/sprites/ship_on.png')),
	'ship_off': center_anchor(pyglet.ressource.image('assets/sprites/ship_off.png')),
	'bg1': center_anchor(pyglet.ressource.image('assets/bg1.png')),
	'bg2': center_anchor(pyglet.ressource.image('assets/bg2.png')),
	'bg3': center_anchor(pyglet.ressource.image('assets/bg3.png'))
}