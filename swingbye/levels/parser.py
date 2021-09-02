if __name__ == '__main__':
	# `python -m swingbye.levels.parser` needs this to run the test
	import pyglet
	pyglet.resource.path = ['../']
	pyglet.resource.reindex()


import pyglet
import logging
from swingbye.cphysics import vec2
# from swingbye.logic.ship import Ship
# from swingbye.logic.planet import Planet
from swingbye.logic.world import World
from swingbye.pygletengine.utils import create_sprite
from swingbye.pygletengine.components.paths import PointPath, LinePath
from swingbye.pygletengine.gameobjects.entities import ShipObject, PlanetObject
from swingbye.pygletengine.globals import GameEntity
from swingbye.globals import PLANET_PREDICTION_N, SHIP_PREDICTION_N

_logger = logging.getLogger(__name__)


def parse_level(level: dict, batch: pyglet.graphics.Batch, group: pyglet.graphics.OrderedGroup) -> World:
	world = World()
	queue = [(child_dict, None) for child_dict in level['world']]

	while queue:
		child_dict, parent = queue.pop()

		# Convert the position list to a vec2
		if 'pos' in child_dict['arguments']:
			child_dict['arguments']['pos'] = vec2(*child_dict['arguments']['pos'])
		if 'anchor' in child_dict['arguments']:
			child_dict['arguments']['anchor'] = vec2(*child_dict['arguments']['anchor'])

		if child_dict['type'] in ['planet', 'wormhole']:
			world.add_planet_existing(PlanetObject(
				sprite=create_sprite(child_dict['sprite'], subpixel=True, batch=batch, group=pyglet.graphics.OrderedGroup(0, parent=group)),
				# TODO: colors
				path=PointPath(batch=batch, point_count=PLANET_PREDICTION_N),
				# TODO : named planets
				# name=child_dict['name'],
				game_entity=GameEntity.PLANET if child_dict['type'] == 'planet' else GameEntity.WORMHOLE,
				**child_dict['arguments']
			))
			world.planets[-1].set_parent(parent)
			queue += [(_child_dict, world.planets[-1]) for _child_dict in child_dict['children']]

		elif child_dict['type'] == 'ship':
			world.add_entity_existing(ShipObject(
				sprite=create_sprite(child_dict['sprite'], anchor='center', subpixel=True, batch=batch, group=pyglet.graphics.OrderedGroup(0, parent=group)),
				path=LinePath(batch=batch, point_count=SHIP_PREDICTION_N),
				**child_dict['arguments']
			))
			world.entities[-1].parent = parent

		else:
			_logger.warning(f'type `{child_dict["type"]}` is not recognized.')

	world.time = 0

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

	print('>>> testing that python methods still exist')
	assert(hasattr(world.planets[-1], 'sprite'))
	print(world.planets[-1].sprite)
	print('OK')
