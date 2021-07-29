import pyglet

def create_sprite(path: str, **kwargs) -> pyglet.sprite.Sprite:
	image = pyglet.resource.image(path)
	image.anchor_x = image.width // 2
	image.anchor_y = image.height // 2
	return pyglet.sprite.Sprite(image, **kwargs)
