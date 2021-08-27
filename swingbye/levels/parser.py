# temporary, remove this
import pyglet
pyglet.resource.path = ['../']
pyglet.resource.reindex()


import pyglet
import logging
from swingbye.cphysics import vec2
# from swingbye.logic.ship import Ship
# from swingbye.logic.planet import Planet
from swingbye.logic.world import World
from swingbye.logic.planet import Planet
from swingbye.pygletengine.utils import create_sprite
from swingbye.pygletengine.components.paths import PointPath, LinePath
from swingbye.pygletengine.gameobjects.entities import ShipObject, PlanetObject
from swingbye.pygletengine.globals import GameEntity

_logger = logging.getLogger(__name__)


def parse_level(level: dict, batch: pyglet.graphics.Batch, group: pyglet.graphics.OrderedGroup) -> World:
	world = World()
	queue = [(child_dict, None) for child_dict in level['world']]

	while queue:
		child_dict, parent = queue.pop()

		# Convert the position list to a vec2
		if 'pos' in child_dict:
			child_dict['pos'] = vec2(*child_dict['pos'])
		if 'anchor' in child_dict:
			child_dict['anchor'] = vec2(*child_dict['anchor'])

		_logger.debug(f'parsing {child_dict}')

		if child_dict['type'] in ['planet', 'wormhole']:
			# Try world.add_planet()
			# then trying to assign a new subclass ?
			world.add_planet(Planet(mass=69))

	return world


if __name__ == '__main__':
	import json
	import pyglet

	with open('swingbye/levels/level1.json') as file:
		level = json.load(file)

	batch = pyglet.graphics.Batch()
	group = pyglet.graphics.OrderedGroup(1)
	world = parse_level(level, batch, group)

	print(world)

	print(world.planets[0].prediction)
