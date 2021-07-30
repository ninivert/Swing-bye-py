import pyglet
from typing import Union


def create_sprite(path: str, anchor='center', size=None, **kwargs) -> pyglet.sprite.Sprite:
	image = pyglet.resource.image(path)
	
	if anchor == 'center':
		image.anchor_x = image.width // 2
		image.anchor_y = image.height // 2
	elif anchor == 'bottom_left':
		image.anchor_x = 0
		image.anchor_y = 0

	if size is not None:
		image.width = size[0]
		image.height = size[1]

	return pyglet.sprite.Sprite(image, **kwargs)

def clamp(value: Union[int, float], mini: Union[int, float], maxi: Union[int, float]) -> Union[int, float]:
	return min(max(value, mini), maxi)

def point_in_rect(x: Union[int, float], y: Union[int, float], rect_x: Union[int, float], rect_y: Union[int, float], width: Union[int, float], height: Union[int, float]):
	return (rect_x <= x <= rect_x + width) and (rect_y <= y <= rect_y + height)
