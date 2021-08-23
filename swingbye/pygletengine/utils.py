import pyglet
from .gameobjects.linepath import LinePath
from .gameobjects.pointpath import PointPath

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

def clamp(value: float, mini: float, maxi: float) -> float:
	return min(max(value, mini), maxi)

def lerp(value: float, target_value: float, t: float) -> float:
	return value + (target_value - value)*t

def point_in_rect(x: float, y: float, rect_x: float, rect_y: float, width: float, height: float) -> bool:
	return (rect_x <= x <= rect_x + width) and (rect_y <= y <= rect_y + height)
