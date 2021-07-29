import pyglet
from typing import Union


def create_sprite(path: str, **kwargs) -> pyglet.sprite.Sprite:
	image = pyglet.resource.image(path)
	image.anchor_x = image.width // 2
	image.anchor_y = image.height // 2
	return pyglet.sprite.Sprite(image, **kwargs)

def clamp(value: Union[int, float], mini: Union[int, float], maxi: Union[int, float]) -> Union[int, float]:
	return min(max(value, mini), maxi)
